---
layout: post
title: "Rete and \"True Modify\""
date: 2010-01-04
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/01/rete-and-true-modify.html
---

### Rete and “True Modify”

The first commit for "true modify" is in, although we’ll need to think of a better name for it. The branch doesn’t fully compile, so you can’t use maven. But it does compile enough to run examples that use just joins, not and exist nodes. Such as manners and waltz. And we’ve been extending the rete testing harness, <http://blog.athico.com/2009/11/rete-dsl-testing-harness.html>, to provide more thorough testing of these nodes. I’ll blog this algorithm in more detail later:  
<http://fisheye.jboss.org/browse/JBossRules/branches/true_modify_20100104>

The crux of it is that a modify no longer is a stateless retract+assert. I use the term stateless here as all state is lost in the retract and all state is recreated in the assert, it’s not easy to know the state changes between these two in a stateful manner.

As an example of work arounds we have had to do, to determine those state changes, take the event model for activations. Drools has always provided activation normalisation, to make the events seem correct and for truth maintenance. When a modify happens we put all cancelled activations in a map, that happened as part of the retract, and remove all activations that are in the map that happaned as part of the assert. This way we can know what was really cancelled, stayed the same and added. While it creates a system users can more easily understand, it adds considerable overhead (about 10%) and complexity, to my knowledge Drools is the only PRD system that does this.

```drl
The new algorithm does not do two propgations, a retract + assert, it instead does a single modify propagation. This propagation applies the constraint and determines what to do and how to continue:
false before, true now = continue as assert
true before, false now = continue as retract
true before, true now = continue as modify
false before, false now = do nothing
```

Tradditional symetrical Rete implementations, such as in Drools 4, would not be able to do this http://blog.athico.com/2008/10/symmetrical-and-asymmetrical-rete.html. Because there is not enough state in the network to avoid the retract + assert. Drools 5.0 implements asymetrical Rete for tree based removal as mentioned in the Doorenbos’s papers and based on the work of Gary Riley in Clips. In this algorithm every Tuple (Jess calls Tokens and Clips calls PartialMatch) knows which Tuples it was joined to and all resulting children, likewise each child knows it’s parents. The implementation alone in Drools 5.0 was not enough to move straight to true modify and the data structures had to be changed, mostly around deterministic iteration. For perf Drools 5 and Clips would just reference the head of a list, we would iterate from the head and add to the head. For true modify the opposite node iterations must be in the same order as the child tuple iterations. To achieve that we need to keep a reference to both the head and the tail, we add to the tail and iterate from the head. Along with a few other additions that means we can now implement modify methods, as illustrated in the JoinNode modifyLeft

```java
public void modifyLeftTuple(final LeftTuple leftTuple,
                            final PropagationContext context,
                            final InternalWorkingMemory workingMemory) {
    final BetaMemory memory = (BetaMemory) workingMemory.getNodeMemory( this );

    // Add and remove to make sure we are in the right bucket and at the end
    // this is needed to fix for indexing and deterministic iteration
    memory.getLeftTupleMemory().remove( leftTuple );
    memory.getLeftTupleMemory().add( leftTuple );

    this.constraints.updateFromTuple( memory.getContext(),
                                      workingMemory,
                                      leftTuple );
    LeftTuple childLeftTuple = leftTuple.firstChild;

    RightTupleMemory rightMemory = memory.getRightTupleMemory();

    RightTuple rightTuple = rightMemory.getFirst( leftTuple );

    // first check our index (for indexed nodes only) hasn't changed and we are returning the same bucket
    if ( childLeftTuple != null && rightMemory.isIndexed() && rightTuple != rightMemory.getFirst( childLeftTuple.getRightParent() ) ) {
        // our index has changed, so delete all the previous propagations
        this.sink.propagateRetractLeftTuple( leftTuple,
                                             context,
                                             workingMemory );

        childLeftTuple = null; // null so the next check will attempt matches for new bucket
    }

    // we can't do anything if RightTupleMemory is empty
    if ( rightTuple != null ) {
        if ( childLeftTuple == null ) {
            // either we are indexed and changed buckets or
            // we had no children before, but there is a bucket to potentially match, so try as normal assert
            for ( ; rightTuple != null; rightTuple = (RightTuple) rightTuple.getNext() ) {
                final InternalFactHandle handle = rightTuple.getFactHandle();
                if ( this.constraints.isAllowedCachedLeft( memory.getContext(),
                                                           handle ) ) {
                    this.sink.propagateAssertLeftTuple( leftTuple,
                                                        rightTuple,
                                                        context,
                                                        workingMemory,
                                                        this.tupleMemoryEnabled );
                }
            }
        } else {
            // in the same bucket, so iterate and compare
            for ( ; rightTuple != null; rightTuple = (RightTuple) rightTuple.getNext() ) {
                final InternalFactHandle handle = rightTuple.getFactHandle();

                if ( this.constraints.isAllowedCachedLeft( memory.getContext(),
                                                           handle ) ) {
                    if ( childLeftTuple != null && childLeftTuple.getRightParent() != rightTuple ) {
                        this.sink.propagateAssertLeftTuple( leftTuple,
                                                            rightTuple,
                                                            context,
                                                            workingMemory,
                                                            this.tupleMemoryEnabled );
                    } else {
                        // preserve the current LeftTuple, as we need to iterate to the next before re-adding
                        LeftTuple temp = childLeftTuple;
                        childLeftTuple = this.sink.propagateModifyChildLeftTuple( childLeftTuple,
                                                                                  rightTuple,
                                                                                  context,
                                                                                  workingMemory,
                                                                                  this.tupleMemoryEnabled );
                        // we must re-add this to ensure deterministic iteration
                        temp.reAddLeft();
                    }
                } else if ( childLeftTuple != null && childLeftTuple.getRightParent() == rightTuple ) {
                    childLeftTuple = this.sink.propagateRetractChildLeftTuple( childLeftTuple,
                                                                               rightTuple,
                                                                               context,
                                                                               workingMemory );
                }
                // else do nothing, was false before and false now.
            }
        }
    }

    this.constraints.resetTuple( memory.getContext() );
}
```

The first thing you’ll notice is that this is about third more code than retract+assert together, and there are additional logic tests to determine the before and after states. This combined with a small overhead addition in the data structures means that actually we aren’t reducing the executed code statements, but increasing. What you’ll notice though is that if there are no state changes, true before and true now, unlike retract+assert it avoids a Tuple creation. So for large conflict sets, where none or only a small proportion of the set changes we get much less or even no object creation and thus reduced load on the GC. In the past large systems with millions of facts using gigabytes of memory have had GC problems, where Drools is creating objects faster than standard GC can keep up with, causing OOME. The answer then was to tune the GC, to make it run more aggressively and more often. For those systems true modify should hopefully be a real advantage. Waltz and manners are small applications and are only marginally faster, most likely only due to the removal of the activation normalisation.

But is it only large systems that will benefit? Not at all. Now that we have stateful modifications it opens up lots of new opportunities for optimisation. The biggest initial gain will be from the more functional programming aspects of Drools. When you use ‘from’ to nest and chain conditional elements and patterns you are using Drools in a functional way. Accumulates are like left folds, it iterates a set of data and produces a derived object which we filter with patterns or other conditional elements.

```
$p : Person( location == "london" )
accumulate( CashFlow( person == $p, type == "DEBIT", $v : value ).
            sum( $v ) )
```

If the Cashflows are all inserted first, the accumulation is triggered by the insertion of a Person. What happens if we change a field on the person, but not the location? In the functional world changes in values for a field are known as side effects. With the traditional Rete approach we have no way of knowing if the side effect can impact the results of the function, more than that the results are wiped away during the retract. With the modify we still have the result, we can then determine if the modified object or field can impact the accumulation, if it doesn’t we can use the result as is, no need to recalculate. Some applications can chain many accumulations in a single rule, the savings in performance here are orders of magnitudes, Drools Planner (was solver) is such an application that will make big gains from this.

Range optimisations, age > $v, normally use BTrees for indexing. If every modify is a retract+assert this would send the BTree rebalancing into over drive, negating any benefits. Now that we can avoid any unnecessary BTree manipulation, range indexing becomes a possibility for Join Nodes.

We can analyse a rule and determine for each object change, at the point that it enters a rule which later nodes depend on this object. We can either avoid unnecessary checks and just propagate to the next node, or just avoid propagation all together. This can all help reduce the amount of work done during the matching phase.

I’m not sure of any literature or other engines that implement this Rete enhancement, so if you know of anything please point me in the right direction.

For a bit of historical information on Drools. In early 2.0 beta releases and in the Drools 3.0 final release there were attempts at “true modify”. The approach in Drools 3.0 meant that each Tuple used Maps and Sets to keep references to matches and children. It worked, but performance was not scalable as memory use went through the roof. Which is why Drools 4.0 returned to a more traditional symmetrical Rete implementation. It’s been a long sought for goal, that we haven’t managed to get right in the past, but feel we are finally there. So I should add, other implementations or literature that worked in scalable way :)
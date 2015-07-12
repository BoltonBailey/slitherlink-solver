# slitherlink-solver

This file implements a solver for the slitherlink puzzle.

## How the slitherlink solver works

Initially, I set the solver to simply go through edges and create a list of partial solutions by copying a partial solution and then setting a particular edge to either be included or not be included in the solution. By pruning branches that violated the rules, this was able to solve some small boards, but was too slow for larger boards.

I then changed the solver to look for edge-decisions that immediately lead to contradictions and to discard those. This solver can now solve very large boards, but could not solve even relatively small boards that were "hard" (as described by puzzle-loop.com, which I use to test the solver). I noticed that the solver will now know how to fill in the determinable lines for a 0 directly adjacent to a 3, but will not do so for patterns such as a 0 and a 3 that share a corner, or two 3's that share a corner. This makes sense, as these latter patterns have no decisions that immediately lead to contradictions (such as a dead end or incorrect number of lines around a numbered block).

My next step will be to tell the solver, when considering an edge, to iteratively look for contradictions resulting from choosing or not choosing that edge. This way, the program can find correct decisions with out creating more branches to the search tree
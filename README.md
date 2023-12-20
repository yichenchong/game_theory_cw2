# Game Theory Coursework 2 - Computational Graph Cram

Cram is an impartial game where two players take turns placing 2-square dominoes onto a grid. Dominoes may not overlap, and the last player to place a domino wins. As with any impartial games, assuming perfect play, one could predict the win or loss of a player based on only the starting position; however, there is no known formula for computing this for Cram, apart from recursively computing nim values for the different game positions, which is an NP problem. This paper introduces a generalisation of Cram, which we call $G$-Cram, based on graph theory, that serves to cut down on the number of positions that need to be evaluated to compute the nim value, and attempts to lay the groundwork for setting a new world record. Proofs for the nim values of some non-trivial base cases are also demonstrated. Finally, the paper solves $G$-Cram for some variants of the game that are not representable in the original Cram game and presents their results.

## Usage

To run the program, simply modify the `GCram.py` file to your liking and run it. The program will output the results to the console.

It should be noted that for large Cram grids (i.e. 5x5 and above), it may take a long time to compute the nim value. For example, a 5x5 grid takes about 10 minutes to compute, and a 6x6 grid takes about 2 hours to compute (at least on my laptop). This is because the program uses a brute-force approach to compute the nim value, and the number of positions to evaluate grows exponentially with the size of the grid. Please be patient, this program is only a prototype!

## Results

The nim values computed by the program are identical to those published by Schneider in his master's thesis, which can be found at "https://github.com/martinschneider/juvavum/blob/master/juvavum_thesis.pdf", and those published by Lemoine et. al, which can be found at https://sprouts.tuxfamily.org/wiki/doku.php?id=records#cram.

However, the key improvement made is reducing the number of positions that need to be stored. This data can be computed in `main.py` (by computing the length of the cache output of nim_values()), or found in `positions.csv` for m-by-n less than 5 by 5 (which are the grid sizes reported by Schneider). They are listed beside the number of positions evaluated by Schneider (again, in the link above) in his thesis.

A result that was not found in our paper that we found with this repository is that the complete graphs appear to have a G-series of period 4 (w/ periodic 0,0,1,1). This makes sense, as the cram minor of a K_n graph is a K_(n-2) graph. A complete graph class and constructor is made available in the GCram.py file.
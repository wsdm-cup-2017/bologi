# -*- coding: utf-8 -*-

"""
Evaluation script for the WSDM Cup 2017 Triple Scoring Task.

Copyright 2016 Unversity of Freiburg
Hannah Bast <bast@cs.uni-freiburg.de>

Usage: python3 evaluator.py --run <file1> --truth <file2> --output <file3>

Compares the scores from file1 (the output of a run) against the scores from
file2 (the ground truth). The three result measures (Accuracy, Average Score
Difference, Average Kendall's Tau) are written to file3 (in protobuf format).

The two score files (file1 and file2) must have an equal number of rows with
exactly three tab-separated columns each (and no tabs otherwise). With respect
to the first two columns, the files must be identical. The third column of each
of the files must be an integer from the range [0..7].

If the two files do not exactly adhere to these formatting rules, the script
will abort with an AssertionError, and a message that specfies how and where the
rules were broken.

The code contains some simple doctest-style unit tests. You can execute them
with python3 -m doctest evaluator.py

"""

import argparse
import itertools
import os
import re


def read_files(filename1, filename2):
    """ Read the two files and check that they adhere to the formatting rules
    described above. If not, exit the program with an error message that
    clarifies the problem. If yes, return two arrays containing the scores from
    the fourth column of file1 and file2 in a list of list, respectively.

    >>> x = open("test1", "w+").write("a\\ta\\t1\\na\\ta\\t2\\nb\\tb\\t3\\n")
    >>> y = open("test2", "w+").write("a\\ta\\t4\\na\\ta\\t5\\nb\\tb\\t6\\n")
    >>> read_files("test1", "test2")
    ([[1, 2], [3]], [[4, 5], [6]])
    >>> os.remove("test1")
    >>> os.remove("test2")
    """

    i = 0
    scores1, scores2 = [], []
    last_subject = None
    with open(filename1) as file1, open(filename2) as file2:
        for line1, line2 in itertools.zip_longest(file1, file2):
            i += 1
            # Check that the lines are formatted correctly and identical, except
            # that the score may differ.
            assert line1 != None, "#lines(file1) < #lines(file2)"
            assert line2 != None, "#lines(file2) < #lines(file1)"
            cols1, cols2 = line1.split("\t"), line2.split("\t")
            line_str = ", at line " + str(i)
            assert len(cols1) == 3, "#columns != 3 in file1" + line_str
            assert len(cols2) == 3, "#columns != 3 in file2" + line_str
            assert cols1[0] == cols2[0], "col1(file1) != col1(file2)" + line_str
            assert cols1[1] == cols2[1], "col2(file1) != col2(file2)" + line_str
            s1, s2 = cols1[2].rstrip(), cols2[2].rstrip()
            check_s1 = re.match("^[0-7]$", s1)
            check_s2 = re.match("^[0-7]$", s2)
            assert check_s1, "score not [0..7] in file1" + line_str
            assert check_s2, "score not [0..7] in file2" + line_str
            # If new subject, start new sublist
            subject = cols1[0]
            if subject != last_subject:
                scores1.append([])
                scores2.append([])
                last_subject = subject
            scores1[-1].append(int(s1))
            scores2[-1].append(int(s2))
    return scores1, scores2


def kendall_tau_ranks(scores):
    """
    Given a list of n scores, return a list of ranks. This is need in function
    kendall_tau below.

    The straightforward result would be to return i for the score that comes
    i-th in the sorted order of scores. If all scores are distinct, this is
    indeed the result returned.  If the same score occurs multiple times, all
    occurrences of that score get the same rank and that rank is the average of
    the ranks they would receive in the straightforward result.

    >>> kendall_tau_ranks([3, 2, 2, 1])
    [4.0, 2.5, 2.5, 1.0]
    """

    # Compute buckets of the same score.
    buckets = {}
    for i, s in enumerate(scores):
        if s not in buckets:
            buckets[s] = []
        buckets[s].append(i)
    # Iterate over buckets and distribute ranks.
    last_rank = 0
    ranks = list(range(0, len(scores)))
    for s in sorted(buckets.keys()):
        n = len(buckets[s])
        # Average ties
        rank = last_rank + ((n + 1) / float(2))
        for i in buckets[s]:
            ranks[i] = rank
        last_rank += n
    return ranks


def kendall_tau(scores1, scores2, p = 0.5):
    """ Compute p-normalized Kendall Tau as described in Fagin et al.  PODS'04
    http://www.cs.uiuc.edu/class/fa05/cs591han/sigmodpods04/pods/pdf/P-06.pdf .
    In the test case below, there are three pairs, all transposed.

    >>> kendall_tau([1, 2, 3], [6, 5, 4])
    1.0
    """

    if len(scores1) == 1:
        return 0.0
    # The ranks of the scores. Equal
    ranks1 = kendall_tau_ranks(scores1)
    ranks2 = kendall_tau_ranks(scores2)
    # All possible pairs i, j with i < j.
    pairs = itertools.combinations(range(0, len(scores1)), 2)
    penalty = 0.0
    # Count the number of pairs in the second list (the ground truth), where
    # pairs with equal scores count only p (default 0.5, see above).
    num_ordered = 0.0
    for i, j in pairs:
        # The ranks of scores i and j in both score lists.
        a_i = ranks1[i]
        a_j = ranks1[j]
        b_i = ranks2[i]
        b_j = ranks2[j]
        # CASE 1: Scores i and j are different in both lists. Then there is a
        # penalty of 1.0 iff the order does not match.
        if a_i != a_j and b_i != b_j:
            if (a_i < a_j and b_i < b_j) or (a_i > a_j and b_i > b_j):
                pass
            else:
                penalty += 1
        # CASE 2: Scores i and j are the same in both lists. Then there is no
        # penalty.
        elif a_i == a_j and b_i == b_j:
            pass
        # CASE 3: Scores i and j are the same in one list, but different in the
        # other. Then there is a penalty of p (default value 0.5, see above).
        else:
            penalty += p
        # Count this pair as 1 if the scores in list 2 are different, otherwise
        # as p (default value 0.5, see above).
        if b_i != b_j:
            num_ordered += 1
        else:
            num_ordered += p
    # Return the average penalty.
    return penalty / num_ordered


def compute_acc(scores1, scores2, delta = 2):
    """ Compute the accuray = the percentage of scores (as a float from [0,1])
    that differ by at most the given delta. If the two score arrays have
    different lengths of contain numbers that are not integers in the range
    [0..7], the result is undefined.

    >>> compute_acc([[1, 2, 3], [4]], [[4, 3, 2], [1]], 1)
    0.5
    """

    num_all = 0
    num_acc = 0
    for group1, group2 in zip(scores1, scores2):
        for score1, score2 in zip(group1, group2):
            num_all += 1
            if abs(score1 - score2) <= delta:
                num_acc += 1
    return num_acc / num_all


def compute_asd(scores1, scores2):
    """ Compute the average score difference. If the two score arrays have
    different lengths of contain numbers that are not integers in the range
    [0..7], the result is undefined.

    >>> compute_asd([[1, 2, 3], [4]], [[4, 3, 2], [1]])
    2.0
    """

    num_all = 0
    sum_difference = 0
    for group1, group2 in zip(scores1, scores2):
        for score1, score2 in zip(group1, group2):
            num_all += 1
            sum_difference += abs(score1 - score2)
    return sum_difference / num_all


def compute_tau(scores1, scores2):
    """ Compute the average p-normalited Kendall tau. If the two score arrays have
    different lengths of contain numbers that are not integers in the range
    [0..7], the result is undefined. For the test case, the tau of the first
    group is 1.0 (all transposed), of the second group 0.0 (single-element).

    >>> compute_tau([[1, 2, 3], [1]], [[3, 2, 1], [4]])
    0.5
    """

    num_groups = len(scores1)
    sum_tau = 0
    for group1, group2 in zip(scores1, scores2):
        sum_tau += kendall_tau(group1, group2)
    return sum_tau / num_groups


""" Main function. """

if __name__ == "__main__":
    # Parse command line arguments.
    parser = argparse.ArgumentParser()
    r = parser.add_argument_group("required arguments")
    r.add_argument("--run", help="File with scores from run.", required=True)
    r.add_argument("--truth", help="File with ground truth.", required=True)
    r.add_argument("--output", help="File with eval results.", required=True)
    args = vars(parser.parse_args())
    filename1 = args["run"]
    filename2 = args["truth"]
    filename3 = args["output"]

    # Read files and count number of triples and subjects. Note that read_files
    # aborts with an assertion error when the two files of not "match" (see
    # above), and in particular when the have a different number of lines.
    scores1, scores2 = read_files(filename1, filename2)
    num_subjects = len(scores1)
    num_triples = sum(len(group) for group in scores1)
    print("Congratulations, the two files were correctly formatted and " +
          "contained matching triples in the same order.")
    print()

    # Evaluate and write result to standard output.
    acc = compute_acc(scores1, scores2)
    asd = compute_asd(scores1, scores2)
    tau = compute_tau(scores1, scores2)
    print("Number of triples        : %d" % num_triples)
    print("Number of subjects       : %d" % num_subjects)
    print()
    print("Accuracy                 : %.2f" % acc)
    print("Average Score Difference : %.2f" % asd)
    print("Average Kendall's Tau    : %.2f" % tau)
    print()
    print("All measures are in [0,1]. For the accuracy, the larger the " +
          "better. For the average score difference and Kendall's Tau, the " +
          "smaller the better.")

    # Write the result to the specified output file, in protobuf format.
    with open(filename3, "w+") as f:
        f.write("measure { key: \"triples\" value: \"%d\" }\n" % num_triples)
        f.write("measure { key: \"subjects\" value: \"%d\" }\n" % num_subjects)
        f.write("measure { key: \"acc\" value: \"%.2f\" }\n" % acc)
        f.write("measure { key: \"asd\" value: \"%.2f\" }\n" % asd)
        f.write("measure { key: \"tau\" value: \"%.2f\" }\n" % tau)
Performance-aggregation-platform---learning-in-near-real-time
=============================================================

The running scores are calculated via Welford's approximation algorithm. See more -
http://bonsai.hgc.jp/~mdehoon/software/python/Statistics/manual/index.xhtml and 
http://stackoverflow.com/questions/5147378/rolling-variance-algorithm

Core Math -:
Initialize M1 = x1 and S1 = 0.

For subsequent x's, use the recurrence formulas

Mk = Mk-1+ (xk - Mk-1)/k 
Sk = Sk-1 + (xk - Mk-1)*(xk - Mk).

For 2 ≤ k ≤ n, the kth estimate of the variance is s2 = Sk/(k - 1).

From here http://www.johndcook.com/standard_deviation.html

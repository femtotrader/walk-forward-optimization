import numpy as np
import pandas as pd


class WalkForwardOptimization:
    def __init__(self, start, end, freq="D", n=7, ins_pct=0.75, anchored=False):
        index = pd.date_range(start, end, freq=freq)
        self.index = index
        self._n = n
        n_index = len(self.index)
        ## Define coefficients of equations
        a = np.array([[1 - ins_pct, -ins_pct], [1, n]])
        b = np.array([0, n_index])
        # Solve equation system
        ins, oos = np.linalg.solve(a, b)
        ins = round(ins)
        oos = round(oos)
        self.ins = ins  # in sample
        self.oos = oos  # oos
        self.anchored = anchored

    @property
    def ins_ratio(self):
        return self.ins / (self.oos + self.ins)

    @property
    def oos_ratio(self):
        return 1 - self.ins_ratio

    @property
    def stages_count(self):
        stage = 0
        for stage, *_ in self.iterate():
            pass
        return stage

    def iterate(self):
        i = 0
        n_index = len(self.index)
        stage = 1
        if self.ins_ratio == 1 and self._n <= 1:
            yield 1, "ins", self.index[0], self.index[-1]
        else:
            while True:
                if i + self.ins < n_index:
                    if i + self.ins + self.oos < n_index:
                        # if i + 2 * self.ins + self.oos < len(index):
                        if self.anchored:
                            yield (
                                stage,
                                "ins",
                                self.index[0],
                                self.index[i + self.ins - 1],
                            )
                            yield (
                                stage,
                                "oos",
                                self.index[i + self.ins],
                                self.index[i + self.ins + self.oos - 1],
                            )
                        else:
                            yield (
                                stage,
                                "ins",
                                self.index[i],
                                self.index[i + self.ins - 1],
                            )
                            yield (
                                stage,
                                "oos",
                                self.index[i + self.ins],
                                self.index[i + self.ins + self.oos - 1],
                            )
                        stage += 1

                        # else:
                        #    yield (index[i], index[i + self.ins - 1]), (index[i + self.ins], index[-1])
                    else:
                        if n_index - (i + self.ins) > self.oos / 2:
                            if self.anchored:
                                if self.ins > 0:
                                    yield (
                                        stage,
                                        "ins",
                                        self.index[0],
                                        self.index[i + self.ins - 1],
                                    )
                                yield (
                                    stage,
                                    "oos",
                                    self.index[i + self.ins],
                                    self.index[-1],
                                )
                            else:
                                if self.ins > 0:
                                    yield (
                                        stage,
                                        "ins",
                                        self.index[i],
                                        self.index[i + self.ins - 1],
                                    )
                                yield (
                                    stage,
                                    "oos",
                                    self.index[i + self.ins],
                                    self.index[-1],
                                )
                        stage += 1
                    i += self.oos
                else:
                    break

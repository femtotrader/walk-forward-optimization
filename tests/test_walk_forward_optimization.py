from pytest import approx
from walk_forward_optimization import WalkForwardOptimization


def test_walk_forward_optimization():
    wfo = WalkForwardOptimization(
        start="2013-01-01", end="2023-01-01", n=7, ins_pct=0.75, anchored=False
    )
    print(f"ins: {wfo.ins}")
    print(f"oos: {wfo.oos}")
    print(f"ins%: {wfo.ins_ratio}")  # 0.8 means 80% in sample / 20% out of sample
    print(f"oos%: {wfo.oos_ratio}")
    assert wfo.ins_ratio == approx(0.75, 0.01)
    assert wfo.oos_ratio == approx(0.25, 0.01)
    for i, (stage, sample, start, end) in enumerate(wfo.iterate(), start=1):
        if i % 2 == 1:
            print(f"Stage: {stage}")
        print(f"\t{sample}: ", start, end, end - start + wfo.index.freq)
    assert stage == 7
    assert wfo.stages_count == 7

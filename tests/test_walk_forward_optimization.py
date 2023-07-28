from pytest import approx
from walk_forward_optimization import WalkForwardOptimization
import pandas as pd


def test_walk_forward_optimization():
    wfo_start = "2013-01-01"
    wfo_end = "2023-01-01"
    wfo = WalkForwardOptimization(
        start=wfo_start, end=wfo_end, n=7, ins_pct=0.75, anchored=False
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


def test_walk_forward_optimization_disabled_ins_only():
    wfo_start = "2013-01-01"
    wfo_end = "2023-01-01"
    wfo = WalkForwardOptimization(
        start=wfo_start, end=wfo_end, n=1, ins_pct=1.0, anchored=False
    )
    print(f"ins: {wfo.ins}")
    print(f"oos: {wfo.oos}")
    print(f"ins%: {wfo.ins_ratio}")  # 0.8 means 80% in sample / 20% out of sample
    print(f"oos%: {wfo.oos_ratio}")
    assert wfo.ins_ratio == approx(1.0, 0.01)
    assert wfo.oos_ratio == approx(0.0, 0.01)
    for i, (stage, sample, start, end) in enumerate(wfo.iterate(), start=1):
        if i == 1:
            assert stage == 1
            assert sample == "ins"
            assert start == pd.to_datetime(wfo_start)
            assert end == pd.to_datetime(wfo_end)
    assert wfo.stages_count == 1


def test_walk_forward_optimization_disabled_oos_only():
    wfo_start = "2013-01-01"
    wfo_end = "2023-01-01"
    wfo = WalkForwardOptimization(
        start=wfo_start, end=wfo_end, n=1, ins_pct=0.0, anchored=False
    )
    print(f"ins: {wfo.ins}")
    print(f"oos: {wfo.oos}")
    print(f"ins%: {wfo.ins_ratio}")  # 0.8 means 80% in sample / 20% out of sample
    print(f"oos%: {wfo.oos_ratio}")
    assert wfo.ins_ratio == approx(0.0, 0.01)
    assert wfo.oos_ratio == approx(1.0, 0.01)
    for i, (stage, sample, start, end) in enumerate(wfo.iterate(), start=1):
        if i == 1:
            assert stage == 1
            assert sample == "oos"
            assert start == pd.to_datetime(wfo_start)
            assert end == pd.to_datetime(wfo_end)
    assert wfo.stages_count == 1

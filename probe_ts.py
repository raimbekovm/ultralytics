import sys, torch
from ultralytics import YOLO
from ultralytics.utils import ASSETS

mode = sys.argv[1]
SOURCE = ASSETS / "bus.jpg"
f = YOLO("yolo26n.pt").export(format="torchscript", imgsz=32, verbose=False)
print(f"== mode={mode} torch={torch.__version__}")
if mode == "predictor":
    m = YOLO(f)
    for i, sz in enumerate([32, 64, 32]):
        m(SOURCE, imgsz=sz, verbose=False)
        print(f"call {i} imgsz={sz} OK predictor.imgsz={m.predictor.imgsz}")
else:
    import torchvision  # noqa
    ts = torch.jit.load(f, map_location="cpu")
    if mode == "freeze":
        ts = torch.jit.freeze(ts.eval())
    if mode == "noprofile":
        torch._C._jit_set_profiling_executor(False)
    x = torch.rand(1, 3, 32, 32)
    for i in range(4):
        if mode == "optexec_off":
            with torch.jit.optimized_execution(False):
                y = ts(x)
        else:
            y = ts(x)
        print(f"run {i} OK shape={tuple(y.shape) if isinstance(y, torch.Tensor) else [tuple(t.shape) for t in y]}")

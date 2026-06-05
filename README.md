# parflowtools-流域裁剪与 PFSOL 生成工具集

## 功能

- 根据 PFBAS 流域编码自动识别对应的流域边界 Shapefile 和模板 GeoTIFF。

- 生成二值掩膜 GeoTIFF（流域内=1，流域外=0）及位置信息 JSON。

- 同时裁剪多个 PFB 文件（slopex, slopey, Shangguan, CONCN_manning, GLHYMPS）。

- 将掩膜转换为 PFB 格式，并调用 `pfmask-to-pfsol` 生成 VTK 和 PFSOL 域文件。

## 安装

### 1. 克隆或上传代码

将项目目录放置于服务器，结构如下：

parflowtools/
├── setup.py
├── environment.yml
├── README.md
└── parflowtools/
    ├── __init__.py
    ├── run_two.py
    ├── generate_mask.py
    └── crop_pfb.py

### 2. 使用 Conda 创建环境（推荐）

```
conda env create -f environment.yaml
conda activate parflowenv
```

### 3. 本地安装

在项目根目录下执行：

```bash
pip install -e .
```

安装后即可使用 `run_two` 命令。

## 依赖

主要依赖通过 conda 自动解决，包括：

- Python 3.9
- geopandas
- rasterio
- pftools
- matplotlib
- numpy

## 配置

运行前请修改 `parflowtools/run_two.py` 中的路径变量：

```python
SHP_DIR = "/data/share/parflow-group/CONCN_Subbasins_Map/PFBAS/shp"
TIF_DIR = "/data/share/parflow-group/CONCN_Subbasins_Map/PFBAS/geotiff"
INPUT_PFB_DIR = "/data/share/parflow-group/CONCN1.1/inputs"
OUTPUT_DIR = "/data/wangzihan-data/outputs"
PFMASK_CMD = "/data/software/parflow-gnu13/parflow-3.13.0/bin/pfmask-to-pfsol"
```

## 使用示例

```bash
run_two
```

程序会提示输入14位流域编码，例如：

```
请输入14位流域编码（如01010105000000）: 01010105000000
```

执行后自动生成以下文件（位于输出目录）：

- `mask.tif`：二值掩膜 GeoTIFF
- `mask.pfb`：掩膜 PFB 文件
- `pos.json`：位置信息
- `domain.vtk` / `domain.pfsol`：域文件
- 裁剪后的 PFB 文件：`slopex.01010105000000.pfb` 等

## 输出目录自定义

默认输出目录为 `/data/wangzihan-data/outputs`。如果您希望将结果保存到其他位置，可以通过设置环境变量 `OUTPUT_DIR` 来覆盖：

```
export OUTPUT_DIR=/your/custom/path
run_two
```

例如，保存到您自己的目录：

```bash
export OUTPUT_DIR=/data/users/$(whoami)/my_outputs
run_two
```

> 注意：请确保目标目录存在且有写入权限。程序不会自动创建父目录，建议提前创建（`mkdir -p /your/custom/path`）。

## 其他环境变量

未来可能支持更多环境变量（如 `SHP_DIR`, `TIF_DIR`, `PFMASK_CMD` 等），目前仅 `OUTPUT_DIR` 可配置。

## 路径一致性

- 输入数据路径（Shapefile、GeoTIFF、PFB 文件）**固定**为服务器公共目录，所有用户一致。
- 无需修改代码即可使用。

## 注意事项

- 本工具仅在 **Linux** 环境下测试，需要 `pfmask-to-pfsol` 可执行文件。
- 确保所有输入文件（Shapefile、GeoTIFF、PFB）存在且路径正确。
- 如果缺少 `pfmask-to-pfsol`，会跳过 VTK/PFSOL 生成但裁剪仍可进行。

## 许可证

内部使用，请联系作者。

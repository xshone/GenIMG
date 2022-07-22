GenIMG
==

## 介绍
自动排列组合生成带透明通道的图层图片，批量生成。

## 如何使用

- output_dir: 输出目录
- assets_dir: 图片素材根目录
- layer_index: 图层层级，1表示最低层
- directory: 图层图片所在目录
- image_mode: 图片模式

```json
{
  "output_dir": ".\\NFT_Faces",
  "assets_dir": ".\\assets",
  "parts": [
    {
      "layer_index": 1,
      "directory": "clothes"
    },
    {
      "layer_index": 2,
      "directory": "face"
    },
    {
      "layer_index": 3,
      "directory": "tattoo"
    },
    {
      "layer_index": 4,
      "directory": "eye"
    }
  ],
  "image_mode": "RGBA"
}
```
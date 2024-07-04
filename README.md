# SplitFiles

A text splitter that splits a large text file into several smaller text files by line.

一个文本分割器，可以将大文本文件按行分割成若干小文本文件。

<!-- markdownlint-disable MD033 -->
<table>
  <tr>
    <td>
      <img src="https://github.com/aoguai/SplitFiles/blob/master/images/0.png"/>
      <br><b>GUI 界面</b>
    </td>
    <td>
      <img src="https://github.com/aoguai/SplitFiles/blob/master/images/1.png"/>
      <br><b>导出效果</b>
    </td>
  </tr>
</table>
<!-- markdownlint-enable MD033 -->

## 介绍

这是一个简单的文本分割器，可以将大文本文件**按行**分割成若干小文本文件。
拥有简单的 GUI 界面

因为我找了一圈没发现简单好用的能实现同需求的分割器，所以干脆自己写了一个，特此分享出来。

### 效率与特点

1. 对中文与特殊符号友好
2. 效率高，速度快


## 部署与使用

### 从项目仓库源码构建

您可以自行从项目仓库源码构建该项目
```bash
git clone https://github.com/aoguai/SplitFiles.git
cd SplitFiles
pip install -r requirements.txt
python GUI.py
```

### GUI 与 可执行文件说明

**如果您是 windows 用户，没有浏览项目代码需求**
可以前往[下载页面](https://github.com/aoguai/SplitFiles/releases)下载打包后的可执行文件。

## 贡献者们

感谢以下贡献者们对本项目作出的贡献:
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="100%"><a href="https://github.com/darnell8"><img src="https://avatars.githubusercontent.com/u/119397407?v=4?s=100" width="100px;" alt="darnell8"/><br /><sub><b>darnell8</b></sub></a><br /><a href="https://github.com/aoguai/SplitFiles/commits/master?author=darnell8" title="Code">💻</a><a href="https://github.com/aoguai/SplitFiles/issues?q=author:darnell8" title="Bug reports">🐛</a><a href="https://github.com/aoguai/SplitFiles/commits/master?author=darnell8" title="Bug reports">🚧</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

您可以直接在 [issues](https://github.com/aoguai/SplitFiles/issues)
中提出您的问题。

同时你可以通过查看 [CONTRIBUTING.md](https://github.com/aoguai/SplitFiles/blob/master/docs/CONTRIBUTING.md)
了解如何贡献您的代码。

### 更新日志


- **2024/07/04 SplitFilesV1.3.0 版本更新**
  - **支持 批量切割文件**
  - **支持 按文件大小切割**
  - 支持 用户选择文件编码格式
  - 支持 切割 jsonl 类型文件
  - 重构 代码结构，使代码更加规范
  - 修复 其他已知BUG

  注意：从 1.3.0 版本开始 Windows7 不在支持。如果你需要在 window7 下使用，请使用 1.3.0 以前的版本

<details> 
    <summary>往期更新日志</summary>

- **2024/01/22 SplitFilesV1.2.0 版本更新**
  - 更新 README
  - **支持 切割 csv 类型文件**
  - 重构 代码结构，使代码更加规范
  - 修复 分割大文件时拖动UI卡顿问题
  - 修复 阻塞主线程BUG，异步化切割线程
- **2023/01/08 SplitFilesV1.1.0 版本更新**
  - 支持 拖拽文件导入路径
- **2023/01/07 SplitFilesV1.0.0 版本更新**
  - 项目 创建
</details>

## License 说明

[SplitFiles](https://github.com/aoguai/SplitFiles) 遵循 [MIT license](LICENSE)。

我们严禁所有通过本程序违反任何国家法律的行为，请在法律范围内使用本程序。

默认情况下，使用此项目将被视为您同意我们的规则。请务必遵守道德和法律标准。

如果您不遵守，您将对后果负责，作者将不承担任何责任！
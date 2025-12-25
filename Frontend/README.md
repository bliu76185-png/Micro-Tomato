# 学术论文图解助手 (Micro Tomato)

一个基于Streamlit的学术论文智能解析与可视化工具，采用吉卜力风格的温暖UI设计，帮助用户快速理解论文内容并生成直观图表。

## 🌟 核心功能

- 📄 **PDF论文上传**: 支持最大100MB的PDF文件上传（演示模式）
- 🔍 **智能内容解析**: 自动展示论文标题、作者、摘要和关键词
- 📊 **示例图例展示**: 生成展示论文行文逻辑的讲解图例
- ⚡ **论文梳理功能**: 一键生成论文逻辑梳理报告
- 📥 **结果下载**: 支持下载论文逻辑梳理报告
- 🎨 **吉卜力风格UI**: 温暖柔和的用户界面设计
- 🎭 **演示模式**: 直接运行即可体验完整功能

## 📊 演示数据

当前演示模式包含以下示例数据：

### 论文信息
- **标题**: 基于深度学习的医疗诊断系统研究
- **作者**: 张三, 李四, 王五
- **发表年份**: 2024
- **页数**: 15页
- **关键词**: 机器学习、医疗诊断、深度学习、人工智能
- **摘要**: 本论文研究了机器学习在医疗诊断中的应用。通过深度学习模型，我们开发了一个能够准确识别疾病的智能诊断系统。实验结果表明，该系统的准确率达到95%，显著优于传统方法。

### 生成图表
1. **生成的若干图片** (``)
<!-- 2. **模型架构图** (`model_architecture.png`): 深度学习网络结构和层次设计
3. **性能指标图** (`performance_metrics.png`): 精确率、召回率和F1分数分析 -->
## 🎭 系统模式

### 演示模式 vs 完整模式

| 特性 | 演示模式 | 完整模式 |
|------|----------|----------|
| 🚀 启动速度 | 快速启动 | 需要后端 |
| 📊 数据真实性 | 模拟演示数据 | 真实处理结果 |
| 📄 文件上传 | 模拟上传 | 支持真实PDF上传 |
| 📥 文件下载 | 示例报告 | 真实生成的文件 |
| 🔧 依赖需求 | 仅需Streamlit | + ChartGalaxy后端 |

## 🖥️ 系统要求

- **操作系统**: Windows, macOS, Linux
- **Python版本**: 3.8+
- **浏览器**: Chrome, Firefox, Safari, Edge (最新版本)
- **网络**: 完整模式需要连接ChartGalaxy后端服务 (http://localhost:5185)

## 安装和运行

### 🎭 方式1：演示模式（推荐首次体验）

无需后端服务，直接体验完整界面：

```bash
pip install streamlit
streamlit run paper_demo.py
```

然后界面将直接进入演示模式，您可以体验所有功能。

### 🔧 方式2：完整模式（需要后端）

#### 1. 安装依赖
```bash
pip install -r requirements.txt
```

#### 2. 启动ChartGalaxy后端服务
```bash
cd ChartGalaxyDemo-main/ChartGalaxyDemo-main
python app.py
```

确保后端服务在 http://localhost:5185 运行

#### 3. 启动Streamlit前端
```bash
streamlit run paper_demo.py
```

应用将在浏览器中打开，通常地址为 http://localhost:8501

### 🚀 方式3：一键启动
```bash
python start.py
```

## 📋 使用指南

### 步骤1: 启动应用
选择以下任一方式启动应用程序

### 步骤2: 浏览演示内容
1. 演示模式自动加载示例论文数据
2. 查看左侧的文件上传区域（演示用途）
3. 中间栏展示解析后的论文基本信息
4. 右侧栏展示AI生成的图例

### 步骤3: 查看论文信息
- **中间栏**显示解析后的论文基本信息
- 包括标题、作者、发表年份、关键词和摘要
- 关键词以横向便签形式展示

### 步骤4: 查看生成图例
- **右侧栏**展示生成的若干讲解图例

### 步骤5: 下载论文梳理报告
1. 点击中间栏的"下载论文逻辑梳理 PDF"按钮
2. 保存包含论文逻辑梳理的报告文件

## 项目结构

```
├── paper_demo.py          # 主应用文件
├── demo.py                # 演示启动脚本
├── start.py               # 一键启动脚本
├── requirements.txt       # Python依赖
├── README.md             # 使用说明
├── temp_uploads/         # 临时上传目录
└── ChartGalaxyDemo-main/ # ChartGalaxy后端项目
```

## 🎨 设计特色

### 吉卜力风格UI设计
- **色彩方案**: 采用温暖的大地色调，如米色(#f5f1e8)、淡绿(#7ba05b)、棕色(#d4a574)
- **字体选择**: 使用Georgia衬线字体，营造优雅感
- **界面元素**: 圆润的按钮、柔和的阴影、渐变背景
- **动画效果**: 平滑的过渡和微妙的脉冲动画
- **三栏布局**: 文件上传区域、论文信息展示、图例展示并排显示

### 用户体验设计
- **单页应用**: 所有功能集成在一个页面中，无需页面跳转
- **固定数据**: 演示模式使用固定的示例数据展示功能
- **响应式设计**: 适配不同屏幕尺寸（待定）（优先PC）
- **友好提示**: 清晰的状态指示和错误提示
- **直观交互**: 拖拽上传、一键下载等便捷操作

## 🏗️ 技术架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    前端界面层 (Streamlit)                   │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│  文件上传区域 │  论文信息展示 │  图例展示    │   下载管理         │
│   模块       │    模块      │   模块       │    模块           │
└─────────────┴─────────────┴─────────────┴───────────────────┘
                              │
                         API 调用层
                              │
┌─────────────────────────────────────────────────────────────┐
│                  后端服务层 (ChartGalaxy)                   │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│  文件处理    │  内容解析    │  AI图表生成  │   结果打包         │
│   服务       │    服务      │   服务       │    服务 （可选）          │
└─────────────┴─────────────┴─────────────┴───────────────────┘
                              │
                        数据存储层
                              │
┌─────────────────────────────────────────────────────────────┐
│                   本地文件系统存储                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  原始PDF    │ │  处理结果    │ │  生成的图表  │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 技术栈详情
- **前端框架**: Streamlit (Python)
- **后端服务**: ChartGalaxy Flask API
- **数据处理**: Pandas, NumPy
- **UI设计**: 自定义CSS样式
- **文件处理**: PyPDF2, pdfplumber
- **图像处理**: Pillow, matplotlib
- **HTTP请求**: requests库
- **状态管理**: Streamlit会话状态

## ⚙️ 配置说明

### 环境变量配置
```bash
# 后端服务地址
BACKEND_URL=http://localhost:5185

# 文件上传大小限制 (MB)
MAX_FILE_SIZE=100

# 临时文件存储路径
TEMP_DIR=./temp_uploads

# 自动刷新间隔 (秒)
REFRESH_INTERVAL=5
```

### 自定义配置
用户可以通过修改 `config.py` 文件自定义以下设置：
- UI主题颜色
- 支持的文件格式
- 处理超时时间
- 默认下载选项

## ⚠️ 注意事项

1. **后端服务**: 完整模式需要ChartGalaxy后端服务正常运行
2. **文件限制**: 上传文件大小限制为100MB，仅支持PDF格式
3. **浏览器兼容**: 推荐使用Chrome或Firefox最新版本
4. **网络环境**: 处理大型论文时需要稳定的网络连接
5. **权限要求**: 首次运行可能需要管理员权限安装依赖

## 🔧 故障排除

### 常见问题及解决方案

#### 后端连接失败
**问题**: 无法连接到ChartGalaxy服务
**解决方案**:
- 检查ChartGalaxy服务是否在5185端口运行
- 确认防火墙设置允许连接
- 验证后端服务是否已正确启动

#### 文件上传失败
**问题**: PDF文件无法上传
**解决方案**:
- 检查文件格式是否为PDF
- 确认文件大小不超过100MB
- 检查临时目录权限
- 尝试刷新页面后重新上传

#### 图表显示异常
**问题**: 生成的图表无法显示或显示不完整
**解决方案**:
- 清除浏览器缓存
- 检查网络连接稳定性
- 确认后端处理任务已完成
- 尝试重新生成图表

#### 下载功能失效
**问题**: 无法下载处理结果
**解决方案**:
- 检查浏览器是否阻止了自动下载
- 确认文件已成功生成
- 尝试右键另存为下载
- 检查浏览器下载设置

### 性能优化建议

1. **大文件处理**: 对于超过50MB的PDF文件，建议在处理前进行页面优化
2. **内存管理**: 长时间使用后建议重启应用释放内存
3. **并发限制**: 同时处理多个任务可能导致性能下降

## 📄 许可证

本项目基于ChartGalaxy项目进行开发，遵循MIT开源许可证。

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发环境搭建
1. 克隆本项目
2. 安装依赖: `pip install -r requirements.txt`
3. 启动开发服务器: `streamlit run paper_demo.py`

### 代码规范
- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档字符串
- 确保所有函数都有单元测试

## 📞 联系方式

- 项目主页: [GitHub Repository]
- 问题反馈: [Issues页面]
- 邮箱联系: [项目邮箱]



openapi: 3.0.3
info:
  title: Micro Tomato API - 学术图解助手
  description: |
    该 API 支持上传论文并生成多个并列的视觉化方案。
    用户可以从生成的多个候选结果中选择最符合审美（如吉卜力风格）或逻辑的一张进行下载。
  version: 1.1.0

paths:
  /papers/analyze:
    post:
      tags:
        - 核心解析
      summary: 解析 PDF 并触发图例生成
      description: 上传文件后，系统会同步开始提取论文信息并并行生成多张备选图。
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
      responses:
        '200':
          description: 解析与图例预生成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaperResponse'

  /papers/{paper_id}/candidates:
    get:
      tags:
        - 图像获取
      summary: 获取并列的备选图结果
      description: 针对同一篇论文，返回多个不同视觉风格或构图的备选图例（非先后顺序）。
      parameters:
        - name: paper_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 返回并列的图片列表
          content:
            application/json:
              schema:
                type: object
                properties:
                  candidates:
                    type: array
                    items:
                      $ref: '#/components/schemas/ImageCandidate'

components:
  schemas:
    PaperResponse:
      type: object
      properties:
        paper_id:
          type: string
          example: "uuid-789-xyz"
        content:
          $ref: '#/components/schemas/PaperContent'

    PaperContent:
      type: object
      properties:
        paper_title:
          type: string
          example: "基于深度学习的医疗诊断系统研究"
        summary:
          type: string
          example: "本论文研究了机器学习在医疗诊断中的应用..."
        # ... 其他 DemoData 字段

    ImageCandidate:
      type: object
      description: 并列的候选图片结果
      properties:
        candidate_id:
          type: integer
          description: 备选方案唯一标识
          example: 1
        style_tag:
          type: string
          description: 该方案的风格或主题描述
          example: "怀旧手绘风"
        image_url:
          type: string
          description: 图片访问地址
          example: "https://picsum.photos/seed/option1/280/180"
        download_payload:
          type: string
          description: 用于下载该特定方案的数据包或元数据
          example: "Candidate_Data_V1"
# Resolution Theorem Prover - 一阶逻辑推理系统

## 👥 项目团队与分工

### 成员A - 算法核心开发（已完成 ✅）
- **clause.py** - 数据结构定义（Term, Literal, Clause）
- **unification.py** - 合一算法实现  
- **resolution.py** - 归结推理核心算法
- **main.py** - 主程序框架

### 成员B - 问题建模与系统集成（待完成 🔄）
- **problems.py** - 问题子句定义与转化
- **test_resolution.py** - 测试用例与验证
- **experiment_log.py** - 实验过程记录
- **实验报告.docx** - 完整实验文档
- **README.txt** - 运行说明文档
- **推理过程日志.txt** - 详细推理步骤

## 📁 最终项目架构

```
resolution_prover/
├── 📊 核心算法（成员A完成）
│   ├── clause.py           # 数据结构定义
│   ├── unification.py      # 合一算法
│   ├── resolution.py       # 归结推理核心
│   └── __init__.py         # 包初始化
│
├── 🔧 系统集成（成员B负责）
│   ├── problems.py         # 问题子句定义
│   ├── test_resolution.py  # 测试用例
│   ├── experiment_log.py   # 实验过程记录
│   └── main.py             # 主程序入口
│
└── 📝 文档输出（成员B负责）
    ├── 实验报告.docx        # 完整实验报告
    ├── README.txt          # 运行说明
    └── 推理过程日志.txt     # 详细推理步骤
```

## 🎯 成员B的具体工作任务

### 任务1：创建 problems.py
**目标**：修正两个逻辑问题的子句表示

```python
# problems.py 需要包含：
def create_howling_hounds_problem_fixed():
    """修正的Howling Hounds问题子句集"""
    # 重新设计子句，确保逻辑正确
    
def create_drug_dealer_problem_fixed():
    """修正的Drug Dealer问题子句集"""
    # 重新设计子句，确保逻辑正确
    
def create_simple_test_cases():
    """创建简单测试用例验证算法"""
    # 用于调试的简单问题
```

### 任务2：创建 test_resolution.py
**目标**：验证算法正确性和性能

```python
# test_resolution.py 需要包含：
def test_simple_contradiction():
    """测试简单矛盾 P ∧ ¬P"""
    
def test_unification():
    """测试合一算法功能"""
    
def test_problem_solutions():
    """测试两个主要问题的求解"""
```

### 任务3：创建 experiment_log.py
**目标**：记录详细的推理过程

```python
# experiment_log.py 需要包含：
class ExperimentLogger:
    def log_step(self, step_info):
        """记录每一步归结过程"""
        
    def generate_report(self):
        """生成实验报告数据"""
        
    def save_to_file(self, filename):
        """保存推理过程到文件"""
```

### 任务4：文档撰写
**目标**：完成所有要求的文档

- **实验报告.docx**：包含实验方法、结果、总结
- **README.txt**：详细的运行环境和方法说明  
- **推理过程日志.txt**：程序运行的详细输出

## 🚀 快速开始指南

### 环境配置
```bash
# 确保Python 3.6+环境
python --version

# 下载项目代码
git clone <repository-url>
cd resolution_prover
```

### 测试当前系统
```bash
# 测试基础功能（确认成员A的代码正常工作）
python check_basic.py

# 测试算法逻辑
python check_algorithms.py

# 运行主程序查看当前状态
python main.py
```

## 🔍 当前问题诊断

### 已知问题：
1. **变量标准化过于激进**：`X_0`, `X_1` 应该是相同变量但被分开处理
2. **问题建模需要修正**：子句表示可能逻辑不正确
3. **推理过程卡住**：复杂问题达到最大步数限制

### 调试建议：

#### 第一步：验证核心算法
```python
# 在 test_resolution.py 中先测试简单情况
def test_simple_case():
    prover = ResolutionProver()
    prover.add_clause(Clause([Literal("P", [])]))           # P
    prover.add_clause(Clause([Literal("P", [], negated=True)]))  # ¬P
    result = prover.two_pointer_resolution()
    # 这个应该返回 True（找到矛盾）
```

#### 第二步：修正问题建模
检查 `problems.py` 中的子句表示：
- Howling Hounds 问题：确保所有条件正确转化
- Drug Dealer 问题：检查Skolem常数使用

#### 第三步：添加调试输出
在 `resolution.py` 中添加进度信息：
```python
# 在 two_pointer_resolution 方法中添加
if self.steps % 100 == 0:
    print(f"进度: {self.steps} 步，当前子句数: {len(self.clauses)}")
```

## 📋 具体实施步骤

### 第1天：搭建基础框架
1. 创建 `problems.py` 文件
2. 创建 `test_resolution.py` 文件  
3. 创建 `experiment_log.py` 文件
4. 运行现有测试确认环境正常

### 第2天：修正问题建模
1. 重新设计Howling Hounds问题的子句
2. 重新设计Drug Dealer问题的子句
3. 创建简单测试用例验证算法

### 第3天：测试与调试
1. 运行测试用例分析问题
2. 添加调试输出观察推理过程
3. 修正发现的逻辑错误

### 第4天：实验记录与文档
1. 运行完整实验记录过程
2. 生成推理过程日志
3. 开始撰写实验报告

### 第5天：完成与提交
1. 完成所有文档
2. 最终测试验证
3. 打包提交作业

## 🛠️ 技术要点提示

### 问题建模关键：
- **Skolem化**：正确处理存在量词
- **变量标准化**：确保相同变量名正确匹配  
- **子句简化**：避免过于复杂的子句表示

### 实验记录要点：
- 记录每一步的归结对和替换
- 统计成功/失败的合一尝试
- 分析算法性能瓶颈

### 文档撰写要求：
- 实验报告需要详细的方法描述
- 包含具体的推理步骤示例
- 分析算法的优缺点和改进建议

## 📞 协作支持

### 需要成员A协助的情况：
- 核心算法层面的bug
- 数据结构使用问题
- 合一算法的理解

### 成员B独立完成：
- 问题建模和子句设计
- 测试用例编写
- 实验过程记录
- 所有文档撰写

## 🎯 成功标准

### 完成标志：
- [ ] `problems.py` 包含正确的问题子句定义
- [ ] `test_resolution.py` 验证算法正确性
- [ ] `experiment_log.py` 完整记录推理过程
- [ ] 实验报告包含所有要求部分
- [ ] README.txt 提供清晰的运行说明
- [ ] 推理过程日志展示详细步骤

---

**最后更新**: 2025-10-XX  
**项目状态**: 核心算法完成，等待系统集成

> 💡 **提示**: 开始工作前，请先运行 `check_basic.py` 确认成员A的代码正常工作，然后专注于你负责的模块开发。
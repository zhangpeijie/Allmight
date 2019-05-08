# AllMight
## 开发环境
### 硬件环境
	树莓派3B
### 软件环境
	Host：Ubuntu  
	Target：Raspbain（待定）  

| 系统名称 | 特点 |  
| ---- | ---- |
|Raspbian|基于Debian，带图形界面，兼容性好和性能优秀|  
|Raspbian Lite|基于Debian，不带图形界面，兼容性好和性能优秀，安装包更小|  
|Ubuntu Mate|界面个性美观|  
|Snappy Core|Ubuntu针对IoT的一个发行版本|  
|Win10 IoT Core|微软官方针对IoT的一个windows版本|  

	依赖库：python官方和第三方库；OpenCV
	中间件：MQTT协议
### 编程环境
	文本编辑器：vi/vim  
	交叉编译工具：gcc-linaro-arm-linux-gnueabihf-raspbian-x64  
	交叉调试工具：gdb/gdbserver
## 需求分析
### 项目名称
	基于树莓派的车牌识别系统
### 项目结构 
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/%E5%9B%BE%E7%89%872.png?raw=true"/><br>关联图</div>
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/%E5%9B%BE%E7%89%871.png?raw=true" height=80% weight=80%/><br>结构图</div>

### 功能需求
	1. 实现摄像头拍摄并定位车牌  
	2. 实现对图片内容的识别，生成车牌号码  
	3. 实现车牌号码的展示
### 软硬件要求
	硬件需求：  
		摄像头：playstation3 eyestation  
		开发板：树莓派3B  
	软件需求：  
		操作系统：RASPBIAN  
		编程环境：python、gcc、g++  
		依赖库：opencv、MQTT、Qt  
		集成开发环境：vim、pycharm、emacs
#构建目标系统

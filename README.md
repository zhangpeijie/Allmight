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
## 构建目标系统
### 默认配置编译内核（使用交叉编译）
    安装必要依赖：sudo apt-get install git bc bison flex libssl-dev
    克隆Linux内核源码：git clone --depth=1 https://github.com/raspberrypi/linux
    克隆交叉编译工具：git clone https://github.com/raspberrypi/tools ~/tools
    更改环境变量：
    echo PATH=\$PATH:~/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin >> ~/.bashrc
    source ~/.bashrc

    加载默认配置：
    cd linux
    KERNEL=kernel7
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig

    执行make：
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs

    挂载SD卡：
    mkdir mnt
    mkdir mnt/fat32
    mkdir mnt/ext4
    sudo mount /dev/sdb1 mnt/fat32
    sudo mount /dev/sdb2 mnt/ext4

    安装到SD卡：
    sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules_install

    拷贝相关文件到SD卡：
    sudo cp mnt/fat32/$KERNEL.img mnt/fat32/$KERNEL-backup.img
    sudo cp arch/arm/boot/zImage mnt/fat32/$KERNEL.img
    sudo cp arch/arm/boot/dts/*.dtb mnt/fat32/
    sudo cp arch/arm/boot/dts/overlays/*.dtb* mnt/fat32/overlays/
    sudo cp arch/arm/boot/dts/overlays/README mnt/fat32/overlays/
    sudo umount mnt/fat32
    sudo umount mnt/ext4

    将SD卡插入树莓派开机，可以正常启动，Linux内核版本由Linux raspberrypi 4.14.79-v7+更新为Linux raspberrypi 4.19.37-v7+；查阅资料得知可能会存在无法启动的问题，原因是boot引导文件与内核版本不匹配，解决方式为将https://github.com/raspberrypi/firmware中的bootcode.bin，fixup.dat，start.elf三个文件拷贝到boot文件夹中替换原文件即可。

### 根据默认配置裁剪内核
    进入menuconfig配置内核：sudo make ARCH=arm CROSS_COMPILE=~/kernel/tools/arm-bcm2708/    gcc-linaro-arm-linux-gnueabihf-raspbian/bin/arm-linux-gnueabihf- menuconfig  
    配置选项  
    General setup  
| 配置 | 原因 |  
| ---- | ---- |  
| Support for paging of anonymous memory (swap)（Y=>N）| 使用交换分区或者交换文件来做为虚拟内存，系统不需要虚拟内存 |
| BSD Process Accounting（Y=>N）| BSD进程记账支持，用户空间程序可以要求内核将进程的统计信息写入一个指定的文件，主要包括进程的创建时间/创建者/内存占用等信息，不必要的功能|
| Export task/process statistics through netlink（Y=>N）| 通过netlink接口向用户空间导出进程的统计信息，不必要的功能 |
| Automatic process group scheduling（Y=>N）| 每个TTY动态地创建任务分组(cgroup)，这样就可以降低高负载情况下的桌面延迟，系统没有桌面 |
| Support initial ramdisks compressed using gzip Support initial ramdisks compressed using bzip2（Y=>N）| 选择一种压缩方式，支持经过gzip压缩的ramdisk或cpio镜像 |
|Support initial ramdisks compressed using LZMA（Y=>N）| 选择一种压缩方式，支持经过gzip压缩的ramdisk或cpio镜像 |
|Support initial ramdisks compressed using XZ（Y=>N）| 选择一种压缩方式，支持经过gzip压缩的ramdisk或cpio镜像 |
|Support initial ramdisks compressed using LZO（Y=>N）| 选择一种压缩方式，支持经过gzip压缩的ramdisk或cpio镜像 |
|Support initial ramdisk/ramfs compressed using LZ4（Y=>N）| 选择一种压缩方式，支持经过gzip压缩的ramdisk或cpio镜像 |
|BUG() support（Y=>N）| 显示故障和失败条件(BUG和WARN)，嵌入式设备一般不需要 |
|Enable ELF core dumps（Y=>N）|内存转储支持，可以帮助调试ELF格式的程序，用于调试和开发用户态程序，不必要的功能|
|Enable VM event counters for /proc/vmstat（Y=>N）|显示较详细的信息(包含各种事件计数器)主要用于调试和统计，不必要的功能|
|Choose SLAB allocator (SLOB (Simple Allocator))|SLOB针对小型系统设计，做了非常激进的简化，以适用于内存非常有限(小于64M)的嵌入式环境|
|Profiling support（Y=>N）|支持对内核进行分析，内核体积将会显著增大，并且运行速度显著减慢|Enable loadable module support|
|Module versioning support（Y=>N）|允许使用为其他内核版本编译的模块，可会造成系统崩溃|
|Source checksum for all modules（Y=>N）|为模块添加"srcversion"字段，以帮助模块维护者准确的知道编译此模块所需要的源文件，从而可以校验源文件的变动，仅内核模块开发者需要它|
|Enable the block layer||
|Macintosh partition map support（Y=>N）|苹果的Macintosh平台使用的分区格式，目标是树莓派|
|Block layer debugging information in debugfs（Y=>N）|调试信息，不必要的功能|
|Processor type and features||
|Timer frequency (300 Hz)|处理多媒体数据选择300Hz较合适|
|Maximum number of CPUs (2-32)|多核处理器支持，CPU最大核数，选择4|
|Memory split (2G/2G user/kernel split)|内存空间，选择内核与用户空间各占2G|
|Device drivers||
|Broadcom STB GISB bus arbiter（Y）|Broadcom总线仲裁器|
|Multimedia support（M）|多媒体支持，作为模块编译|
|Sound card support（M=>N）|声卡支持，不需要的功能|
|Block devices（M）|块设备支持，作为模块编译|
|SPI support（M）|SPI支持，SD卡可使用SPI，作为模块编译|
|USB support（M）|USB支持，USB设备需要，作为模块编译|
|SCSI device support（M）|SCSI协议支持，作为模块编译|
|LED Class Support（M）|LED支持，作为模块编译|
|Executable file formats / Emulations||
|Enable core dump support（Y=>N）|核心转储(core dump)支持，用于应用程序的调试和开发，不必要的功能
|Filesystems||
|Dnotify support（Y=>N）|旧式的基于目录的文件变化的通知机制(已被Inotify取代)，不需要的功能|
|Print quota warnings to console (OBSOLETE)（Y=>N）|将QUOTA的警告信息直接显示在控制台上，不必要的功能|
|Old quota format support（Y=>N）|老旧的v1版配额格式(linux-2.4.22之前使用的格式)支持|
|Network File Systems（M=>N）|网络文件系统，不需要的功能|
|Miscellaneous filesystems（M=>N）|各种非主流的杂项文件系统，不需要的功能|
|MSDOS fs support（M=>N）|MSDOS文件系统(FAT16)，不需要的功能|
|CD-ROM/DVD Filesystems（M=>N）|CD-ROM/DVD光盘文件系统，不需要的功能|
|JFS filesystem support（M）|JFS文件系统，作为模块编译|
|XFS filesystem support（M）|XFS文件系统，作为模块编译|
|Overlay filesystem support（M）|Overlay 文件系统，作为模块编译|
|VFAT (Windows-95) fs support（M）|FAT32文件系统，作为模块编译|
|NTFS file system support（M）|NTFS文件系统，作为模块编译|
|Virtualization（Y=>N）|虚拟化，系统不需要的功能，不编译进内核|
|Kernel hacking（Y=>N）|内核分析，系统不需要的功能，不编译进内核|
|Networking support（Y=>N）|网络支持，系统本地处理，不需要网络功能，不编译进内核|
    按照上述默认配置编译内核的方法将裁剪后的内核编译安装到树莓派，可以正常运行，
    裁剪前Linux内核大小为5.2M，裁剪后内核大小减小为3.1M
### 加载与卸载至少一个模块程序
    首先用lsmod命令查看已经安装好的模块，得到如下结果：
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_1.png?raw=true"/><br></div>
    然后用 lsmod | grep "media"命令进一步查看media模块的信息：
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_2.png?raw=true"/><br></div>
    这里我特别检查了media模块的相关信息，然后利用modinfo命令查看media模块的具体信息：
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_3.png?raw=true"/><br></div>
    insmod 加载模块，需要指定完整的路径和模块名字 模块依赖及路径信息，这样子才可以成功加载需要模块。查看模块依赖关系可用modinfo查看，利用上文可以看出media模块的路径是 /lib/modules/4.9.80-v7+/kernel/drivers/media/media.ko
    为了保证树莓派正常运行，选择一个没有用上的module进行实验，这个module是i2c_dev，这个module的相关信息如下所示：
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_4.png?raw=true"/><br></div>
    i2c_dev的路径是：/lib/modules/4.9.80-v7+/kernel/drivers/i2c/i2c-dev.ko，因为这个module已经存在了，我首先将这个module删除，再用lsmod命令观察是否将这个module卸载，如图所示：
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_5.png?raw=true"/><br></div>
    如此图所示，将i2c-dev删除后，观察列表中已经没有i2c-dev这个module了，然后利用insmod命令将这个module重新加载，而后利用lsmod命令观察是否将module成功加载，如下图所示：
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_6.png?raw=true"/><br></div>
    可以观察到，这个module已经加载成功。
    这样，就成功加载与卸载了i2c-dev这个模块程序。  

### 创建用于应用开发的文件系统
    对于创建文件系统，思路是首先要对某个ram磁盘进行分区，然后进行文件系统的创建，最后将磁盘挂载到操作系统上的某个目录。
    首先进行磁盘分区，首先进入root获得更大权限以查看磁盘情况，如图所示：
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hm3_7.png?raw=true"/><br></div>
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_8.png?raw=true"/><br></div>
    为了预防操作错误的影响，使用ram14进行进一步的实验，输入：fdisk /dev/ram14表示的是对ram14磁盘进行分区，然后再输入m查看帮助，最后再输入p可以查看该磁盘的分区情况。
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_9.png?raw=true"/><br></div> 
    在输入“p”中可以看出，此时RAM14还没有分区，输入n创建一个新的分区，如图所示：
 <div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_10.png?raw=true"/><br></div>
    从上图可以看出，选择的是默认的设置，即：创建了一个主分区，起始和截止位置都是选择了最前和最后，创建的这个分区占满了ram14，最后输入“p”观察建立的分区的情况，与刚才进行对比，在图中（红框）可以看出已经建立了一个分区。 
    操作系统通过文件系统管理文件及数据，磁盘或分区需要创建文件系统之后才能够为操作系统使用，  输入：mke2fs -t ext4 /dev/然14（用命令mke2fs为ram4分区创建文件系统）
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_11.png?raw=true"/><br></div>
    而后需要挂载文件系统，输入:mount /dev/ram14    /mnt(把ram14分区挂载到mnt上)，并利用mount查看结果：
<div align=center><img src="https://github.com/zhangpeijie/Allmight/blob/master/README.md%20picture/hw3_12.png?raw=true"/><br></div>
    如红框显示，已经将文件系统创建并挂载

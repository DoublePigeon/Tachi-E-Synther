# Tachi-E Synther

 在从各类游戏里得到的差分立绘中，时常会出现一张CG或立绘被分为一个主要图片和若干组件的情况，这时需要组合一张主要图片和一张或多张组件才能得到可使用的完整图片，如果手动进行这个过程，那么对于差分较多的CG来说，工作量将是毁灭性的。因此我创建了这个简单的小脚本来帮助完成这件事情，其功能如下：

- 一次可以选择一张主要图片
- 一次可以选择多张组件
- 可以通过调整参数来改变组件放置的位置，这个参数会同等地作用在所有组件上；并且提供一个预览来实时查看效果
- 每一次合成时，会遍历所有的组件，每一次将一个组件和一个主要图片组合得到一张新图片，然后输出到指定的文件夹

在运行app.py后，只需进入终端提示的URL即可进入webUI

*English*

When extracting character sprites or CGs from various games, it is common to find a "base" image accompanied by several separate component layers (such as expressions or clothing variations). To get a complete, usable image, the base must be merged with one or more of these components. Doing this manually for sets with numerous variations can be an overwhelming and tedious task.

To streamline this process, I created this simple webUI. Its key features include:

- You can select one base image at a time.
- You can select multiple component layers simultaneously.
- You can adjust the placement coordinates of components by changing two parameters; these parameters apply uniformly to all selected parts; A preview is provided so that you can know what the results will be.
- The script iterates through every selected component, merging each with the base image to generate a new variation, and saves the results to a designated folder.

Once you have run app.py, simply click into the URL shown in the terminal and you can enter webUI
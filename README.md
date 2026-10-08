# Tachi-E Synther

 在从各类游戏里得到的差分立绘中，时常会出现一张CG或立绘被分为一个主要图片和若干组件的情况，这时需要组合一张主要图片和一张或多张组件才能得到可使用的完整图片，如果手动进行这个过程，那么对于差分较多的CG来说，工作量将是毁灭性的。因此我创建了这个简单的小脚本来帮助完成这件事情，其功能如下：

- 一次可以选择一张主要图片
- 一次可以选择多张组件
- 可以通过调整参数来改变组件放置的位置，这个参数会同等地作用在所有组件上；并且提供一个预览来实时查看效果
- 提供套索选区：在预览画布上依次点击画出首尾相接的多边形（点击起点处的判定圈闭合），只有在选区内的组件像素才会参与合成；支持新建/增选/减选，且该选区对所有组件同时生效
- 套索采用「草稿 → 应用」两步：画完的多边形先只是草稿（只显示边界，不影响合成），点击「应用套索」后才生效，一次使用可以画多个多边形一起应用；每次应用会分配一种颜色以便区分多次套索的使用，「重置套索」可清空全部已应用的套索
- 显示模式可一键切换：「边界模式」显示完整原图与套索边界（默认，便于编辑），「pixel-faithful」只显示真实的裁剪合成结果
- 每一次合成时，会遍历所有的组件，每一次将一个组件和一个主要图片组合得到一张新图片，然后输出到指定的文件夹

在运行app.py后，只需进入终端提示的URL即可进入webUI

*English*

When extracting character sprites or CGs from various games, it is common to find a "base" image accompanied by several separate component layers (such as expressions or clothing variations). To get a complete, usable image, the base must be merged with one or more of these components. Doing this manually for sets with numerous variations can be an overwhelming and tedious task.

To streamline this process, I created this simple webUI. Its key features include:

- You can select one base image at a time.
- You can select multiple component layers simultaneously.
- You can adjust the placement coordinates of components by changing two parameters; these parameters apply uniformly to all selected parts; A preview is provided so that you can know what the results will be.
- A lasso tool lets you click out a closed polygon directly on the preview canvas (click the handle at the first vertex to close it); only the component pixels inside the region are composited. It supports new/add/subtract selection and applies to every component at once.
- The lasso is a two-step "draft then apply" flow: a closed polygon starts as a draft that only draws its outline, and it takes effect once you press "应用套索" (Apply lasso). Several polygons drawn in one go can be applied together, and each apply gets its own colour so multiple lasso uses stay distinguishable; "重置套索" (Reset lasso) clears every applied lasso.
- A display toggle switches between the boundary mode (full original image plus lasso boundaries, the default, convenient while editing) and a pixel-faithful mode that shows only the real cropped compositing result.
- The script iterates through every selected component, merging each with the base image to generate a new variation, and saves the results to a designated folder.

Once you have run app.py, simply click into the URL shown in the terminal and you can enter webUI
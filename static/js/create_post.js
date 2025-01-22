 const imageUpload = document.getElementById('image-upload');
        const imagePreviews = document.getElementById('image-previews');
        let selectedFiles = [];

        // 处理文件选择
        imageUpload.addEventListener('change', () => {
            // 遍历选择的文件
            Array.from(imageUpload.files).forEach(file => {
                selectedFiles.push(file);  // 保存文件到数组

                // 创建一个新的 FileReader 对象来读取文件
                const reader = new FileReader();

                reader.onload = function (e) {
                    // 创建一个新的 div 来包裹 img 元素
                    const previewDiv = document.createElement('div');
                    previewDiv.classList.add('image-preview');

                    // 创建一个新的 img 元素来显示预览图
                    const img = document.createElement('img');
                    img.src = e.target.result;  // 设置图像源为读取到的结果
                    img.title = "点击删除此图片";  // 鼠标悬停显示文字
                    previewDiv.appendChild(img);

                    // 创建删除按钮
                    const deleteBtn = document.createElement('button');
                    deleteBtn.type = 'button';
                    deleteBtn.classList.add('delete-btn');
                    deleteBtn.textContent = 'X';
                    deleteBtn.onclick = () => deleteImage(deleteBtn);
                    previewDiv.appendChild(deleteBtn);

                    // 将预览图添加到图片预览区域
                    imagePreviews.appendChild(previewDiv);
                };

                // 读取文件数据
                reader.readAsDataURL(file);
            });
        });

        // 删除图片函数
        function deleteImage(button) {
            // 找到图片预览的父元素（div），并删除它
            const previewDiv = button.closest('.image-preview');
            previewDiv.remove();

            // 删除文件数组中的该图片
            const index = Array.from(imagePreviews.children).indexOf(previewDiv);
            selectedFiles.splice(index, 1);  // 从数组中移除该文件
        }

        // 给已上传的图片添加点击选中效果
        const uploadedImages = document.querySelectorAll('.image-preview');
        uploadedImages.forEach(imagePreview => {
            imagePreview.addEventListener('click', () => {
                imagePreview.classList.toggle('selected');
            });
        });

        // 当表单提交时，将所有选择的文件添加到表单数据中
        document.getElementById('post-form').addEventListener('submit', function (e) {
            // 通过 JavaScript 动态添加文件到表单数据中
            const formData = new FormData(this);
            selectedFiles.forEach(file => {
                formData.append('images', file);  // 将所有图片添加到表单数据中
            });

            const submitButton = document.querySelector('button[type="submit"]:focus');  // 获取被点击的按钮
            if (submitButton) {
                formData.append(submitButton.name, submitButton.value || submitButton.textContent.trim());
            }

            // 阻止默认提交，使用自定义的提交方式
            e.preventDefault();
            console.log('到这了')

            // 提交表单
            fetch(this.action, {
                method: 'POST',
                body: formData
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      window.location.href = "{% url 'blog:my_posts' %}";
                  } else {
                      alert('上传失败了，请重试');
                  }
              })
              .catch(error => alert('上传错误，请重试'));
        });
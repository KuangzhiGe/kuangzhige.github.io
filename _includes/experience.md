<h2 id="experience" style="margin-bottom: 20px; ">Education</h2>

<div class="experience">
<ol class="experience-list" style="list-style-type: none; padding: 0; margin: 0;">

{% for item in site.data.experience.main %}

<li style="margin-bottom: 20px; display: flex; align-items: flex-start;">
  <!-- 列表符号 -->
  <span style="font-size: 8px; color: #ffffff; margin-right: 10px;">●</span>

  <!-- 图片和内容 -->
  <div style="display: flex; align-items: center;">
    <!-- 图片部分 -->
    <div style="margin-right: 15px;">
      <img src="{{ item.image }}" alt="{{ item.title }}" style="width: 50px; height: 50px; border-radius: 50%;">
    </div>
    <!-- 内容部分 -->
    <div>
      <div class="title" style="font-size: 18px; font-weight: bold; color: #ffffff;">{{ item.title }}</div>
      <ul style="list-style-type: circle; padding-left: 20px; margin: 5px 0 0;">
        <li style="font-size: 14px; color: #bbbbbb;">{{ item.details }}</li>
      </ul>
    </div>
  </div>
</li>
{% endfor %}

</ol>
</div>

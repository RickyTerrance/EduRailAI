<template>
  <div id="app">
    <header class="header">
      <h1>EduInfo</h1>
      <nav>
        <ul>
          <li><a href="#">FAQ</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <section v-for="post in posts" :key="post.id" class="post" v-bind:style="postStyle">
        <header class="post-header">
          <div class="post-category">{{ post.title }}</div>
        </header>
        <h2 class="post-title">{{ post.site }}</h2>
        <p class="post-content">xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</p>
        <h2 class="post-title">{{ post.email }}</h2>
        <p class="post-content">xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</p>
        <h2 class="post-title">{{ post.phone }}</h2>
        <p class="post-content">xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</p>
        <h2 class="post-title">{{ post.fax }}</h2>
        <p class="post-content">xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</p>
        <footer class="post-footer">
          <div class="post-category">{{ post.title }}</div>
        </footer>
      </section>

      <!-- 教育平台卡片 -->
      <section class="post" v-bind:style="postStyle">
        <header class="post-header">
          <div class="post-category">教育平台</div>
        </header>
        <h2 class="post-title">線上學習</h2>
        <ul class="post-content">
          <li><a href="https://www.coursera.org" target="_blank">Coursera</a></li>
          <li><a href="https://www.edx.org" target="_blank">edX</a></li>
          <li><a href="https://www.udemy.com" target="_blank">Udemy</a></li>
          <li><a href="https://www.khanacademy.org" target="_blank">Khan Academy</a></li>
          <li><a href="https://www.skillshare.com" target="_blank">Skillshare</a></li>
          <li><a href="https://www.futurelearn.com" target="_blank">FutureLearn</a></li>
        </ul>
      </section>

      <!-- 人力資源卡片 -->
      <section class="post" v-bind:style="postStyle">
        <header class="post-header">
          <div class="post-category">人力資源平台</div>
        </header>
        <h2 class="post-title">求職與職業發展</h2>
        <ul class="post-content">
          <li><a href="https://www.linkedin.com" target="_blank">LinkedIn</a></li>
          <li><a href="https://www.104.com.tw" target="_blank">104 人力銀行</a></li>
          <li><a href="https://www.1111.com.tw" target="_blank">1111 人力銀行</a></li>
          <li><a href="https://www.indeed.com" target="_blank">Indeed</a></li>
          <li><a href="https://www.glassdoor.com" target="_blank">Glassdoor</a></li>
          <li><a href="https://www.monster.com" target="_blank">Monster</a></li>
        </ul>
      </section>

      <!-- 專業資源卡片 -->
      <section class="post" v-bind:style="postStyle">
        <header class="post-header">
          <div class="post-category">專業技能提升</div>
        </header>
        <h2 class="post-title">專業資源</h2>
        <ul class="post-content">
          <li><a href="https://www.pluralsight.com" target="_blank">Pluralsight</a></li>
          <li><a href="https://www.codecademy.com" target="_blank">Codecademy</a></li>
          <li><a href="https://www.microsoft.com/en-us/learning" target="_blank">Microsoft Learn</a></li>
          <li><a href="https://aws.amazon.com/training" target="_blank">AWS Training</a></li>
          <li><a href="https://trailhead.salesforce.com" target="_blank">Salesforce Trailhead</a></li>
          <li><a href="https://learn.adobe.com" target="_blank">Adobe Learning</a></li>
        </ul>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "EduRAIL",
  data() {
    return {
      posts: [
        {
          id: 1,
          title: "聯絡我們",
          site: "地址",
          email: "電子郵件",
          phone: "電話",
          fax: "傳真",
          linktitle: "相關網站"
        }
      ],
    };
  },
  computed: {
    postStyle() {
      return {
        transform: "scale(0.95)",
        transition: "transform 0.3s ease",
      };
    },
  },
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f7f7f7;
}

.header {
  background-color: rgb(60, 18, 73);
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.header h1 {
  margin: 0;
  font-size: 1.8rem;
  letter-spacing: 1px;
}

.header nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
}

.header nav ul li {
  margin: 0 0.5rem;
}

.header nav ul li a {
  color: white;
  text-decoration: none;
  font-size: 1rem;
}

.main {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.post {
  background: white;
  margin: 1rem 0;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.post-category {
  font-weight: bold;
  color: #6610f2;
  font-size: 1.2rem;
}

.post-title {
  margin: 0;
  font-size: 1.4rem;
  color: #333;
}

.post-content {
  margin: 1rem 0;
  color: #555;
  font-size: 1rem;
  line-height: 1.6;
}

.post-content ul {
  list-style-type: disc;
  padding-left: 1.5rem;
}

.post-content ul li {
  margin: 0.5rem 0;
}

.post-content ul li a {
  color: white;
  background: linear-gradient(90deg, #6535b3, #8a63f2);
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  text-decoration: none;
  font-size: 1rem;
  display: inline-block;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.post-content ul li a:hover {
  background: linear-gradient(90deg, #8a63f2, #6610f2);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
  text-decoration: none;
}


.post-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.save-btn {
  background-color: #6610f2;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.save-btn:hover {
  background-color: #550dc4;
}
</style>

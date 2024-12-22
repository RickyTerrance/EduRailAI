<template>
  <div id="app">
    <header class="header">
      <h1>EduSpace </h1>
      <nav>
        <ul>
          <li><a href="#">熱門</a></li>
          <li><a href="#">按讚的文章</a></li>
          <li><a href="#">個人頁面</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <section v-for="post in posts" :key="post.id" class="post" v-bind:style="postStyle">
        <header class="post-header">
          <div class="post-category">{{ post.category }}</div>
          <div class="post-time">{{ post.time }}</div>
        </header>
        <h2 class="post-title">{{ post.title }}</h2>
        <p class="post-content">{{ post.content }}</p>
        <footer class="post-footer">
          <div class="post-actions">
            <button @click="toggleReaction(post, 'likes')">❤️ {{ post.likes }}</button>
            <button @click="toggleReaction(post, 'laugh')">😆{{ post.laugh }}</button>
            <button @click="toggleReaction(post, 'surprise')">😲{{ post.surprise}}</button>
            <button @click="toggleReaction(post, 'cry')">😢 {{ post.cry }}</button>
            <button>💬 {{ post.comments }}</button>
          </div>
          <button class="save-btn">收藏</button>
        </footer>
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
          category: "職場",
          time: "23小時前",
          title: "對自己的軟硬實力不清楚或沒有信心",
          content:
            "已經換了三份工作，但每一份都做不久，這讓我對自己開始感到質疑...",
          likes: 1536,
          laugh: 0,
          surprise: 29,
          cry: 107,
          comments: 107,
        },
        {
          id: 2,
          category: "學習",
          time: "5小時前",
          title: "#發問 轉職後該往哪發展？",
          content:
            "目前擔任IT人員，剛從外面的培訓班學習了六個月的前端和C# ...",
          likes: 152,
          laugh: 2,
          surprise: 7,
          cry: 16,
          comments: 16,
        },
        {
          id: 3,
          category: "學習",
          time: "1天前",
          title: "學習歷程攻略",
          content:
            "坦白說，在許多時候，關於學習未來的方向也會感到迷茫...",
          likes: 120,
          laugh: 25,
          surprise: 3,
          cry: 10,
          comments: 12,
        },
        {
          id: 4,
          category: "職場",
          time: "2天前",
          title: "如何有效提升工作效率",
          content:
            "最近我開始使用番茄鐘工作法，發現專注力和效率都提升了許多...",
          likes: 230,
          laugh: 3,
          surprise: 72,
          cry: 15,
          comments: 45,
        },
        {
          id: 5,
          category: "學習",
          time: "3小時前",
          title: "推薦一些免費的線上課程資源",
          content:
            "我發現很多免費的平台提供高質量的線上課程，像是Coursera、edX等等...",
          likes: 95,
          laugh: 8,
          surprise: 19,
          cry: 5,
          comments: 18,
        },
        {
          id: 6,
          category: "生活",
          time: "4天前",
          title: "維持工作與生活平衡的心得",
          content:
            "在快節奏的工作環境中，我發現每天安排一些個人時間非常重要...",
          likes: 180,
          laugh: 11,
          surprise: 75,
          cry: 12,
          comments: 32,
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
  methods: {
    toggleReaction(post, type) {
      if (type === "likes") post.likes++;
      else if (type === "dislikes") post.dislikes++;
      else if (type === "laugh") post.laugh++;
      else if (type === "surprise") post.surprise++;
      else if (type === "cry") post.cry++;
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
  background-color:rgb(60, 18, 73);
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
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
}

.main {
  padding: 1rem;
}

.post {
  background: white;
  margin: 1rem 0;
  padding: 0.8rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.post:hover {
  transform: scale(1.05);
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.post-category {
  font-weight: bold;
  color: #6610f2;
}

.post-time {
  color: gray;
  font-size: 0.9rem;
}

.post-title {
  margin: 0;
  font-size: 1rem;
}

.post-content {
  margin: 0.5rem 0;
  color: #555;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-actions button {
  background: none;
  border: none;
  cursor: pointer;
  color: gray;
  margin-right: 0.5rem;
}

.save-btn {
  background-color: #6610f2;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn:hover {
  background-color: #550dc4;
}
</style>

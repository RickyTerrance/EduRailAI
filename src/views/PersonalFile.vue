<template>
  <div id="app">
    <header class="header">
      <h1>個人檔案</h1>
      <nav>
        <ul>
          <li><a href="#">首頁</a></li>
          <li><a href="#">關於我</a></li>
          <li><a href="#">聯繫方式</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <section class="profile">
        <div class="profile-header">
          <img src="" alt="Profile Picture" class="profile-picture">
          <h2 class="profile-name">User</h2>
          <p class="profile-title">全端工程師 | 技術愛好者 | 持續學習者</p>
        </div>

        <div class="profile-details">
          <section class="about-me">
            <h3>關於我</h3>
            <p>
              我是一名熱愛技術的全端工程師，專注於開發高效能的網站與應用程式。擁有多年經驗，熟悉多種技術框架，
              並持續學習以跟上最新趨勢。
            </p>
          </section>

          <section class="skills">
            <h3>技能</h3>
            <ul>
              <li>JavaScript (ES6+), HTML, CSS</li>
              <li>Vue.js, React, Angular</li>
              <li>Node.js, Express</li>
              <li>Python, Django, Flask</li>
              <li>SQL, MongoDB</li>
              <li>Docker, Kubernetes, CI/CD</li>
            </ul>
          </section>

          <section class="experience">
            <h3>工作經歷</h3>
            <div class="job">
              <h4>資深全端工程師</h4>
              <p>TechCorp Inc. | 2020 - 現在</p>
              <ul>
                <li>領導團隊開發企業級應用程式，提升了系統性能 30%。</li>
                <li>設計與實現跨平台解決方案，滿足多種用戶需求。</li>
                <li>指導初級工程師，分享最佳實踐。</li>
              </ul>
            </div>
            <div class="job">
              <h4>全端工程師</h4>
              <p>CodeStudio | 2017 - 2020</p>
              <ul>
                <li>開發和維護客戶網站，確保高可用性和響應速度。</li>
                <li>與設計團隊合作，創建直觀的用戶體驗。</li>
                <li>實施測試驅動開發 (TDD) 方法，減少了 25% 的錯誤。</li>
              </ul>
            </div>
          </section>

          <section class="education">
            <h3>教育背景</h3>
            <p>計算機科學學士 | XXXX大學 | 2013 - 2017</p>
          </section>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "UserProfile",
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f9f9f9;
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
  margin: 0 1rem;
}

.header nav ul li a {
  color: white;
  text-decoration: none;
}

.profile {
  max-width: 800px;
  margin: 2rem auto;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.profile-header {
  text-align: center;
  margin-bottom: 2rem;
}

.profile-picture {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-bottom: 1rem;
}

.profile-name {
  margin: 0;
  font-size: 1.5rem;
}

.profile-title {
  margin: 0.5rem 0 0;
  color: gray;
  font-size: 1rem;
}

.profile-details section {
  margin-bottom: 1.5rem;
}

.profile-details h3 {
  margin-bottom: 0.5rem;
  color: #34495e;
}

.skills ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.skills ul li {
  background: #ecf0f1;
  margin: 0.5rem 0;
  padding: 0.5rem;
  border-radius: 4px;
}

.job {
  margin-bottom: 1rem;
}

.job h4 {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
}

.job p {
  margin: 0.2rem 0 0.5rem;
  color: gray;
}

.job ul {
  list-style: disc;
  padding-left: 1.5rem;
}

.education {
  text-align: center;
}
</style>

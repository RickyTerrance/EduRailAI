<template> 
  <div id="app"> 
    <!-- 頂部標題 -->
    <header class="header">
      <div class="title">性向測驗對比分析</div>
      <nav class="nav">
        <a href="#">更多相關說明</a>
      </nav>
    </header>
    <!-- 主內容 -->
    <main>
      <!-- 樹狀圖的SVG容器 -->
      <svg ref="treeSvg" :width="width" :height="height"></svg>
      <!-- 樹狀圖的卡片說明 -->
      <div class="card">
        <h2>樹狀圖說明</h2>
        <p>
          本樹狀圖展示了一個中心主題及其多層次的職業或概念分支，代表各種專業發展方向與相關領域。
        </p>
      </div>
    </main>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
 data() {
  return {
    width: 1250,
    height: 900,
    // 樹狀圖的數據（增加更多層次，讓樹變得更豐富）
    treeData: {
      name: "職業發展樹",
      children: [
        {
          name: "資訊工程領域",
          children: [
            { name: "資安鑑識工程師" },
            { name: "後端工程師" },
            { name: "前端工程師" },
            { name: "DevOps 工程師" },
            { name: "資料科學家" },
            { name: "網路安全分析師" },
            { name: "區塊鏈開發工程師" },
            { name: "人工智慧開發" },
          ],
        },
        {
          name: "機械工程領域",
          children: [
            { name: "機械設計工程師" },
            { name: "自動化工程師" },
            { name: "IoT 物聯網硬體整合工程師" },
            { name: "設備維護工程師" },
            { name: "機構研發工程師" },
            { name: "製程工程師" },
          ],
        },
        {
          name: "運輸與物流領域",
          children: [
            {
              name: "交通與工程",
              children: [
                { name: "交通工程師" },
                { name: "運輸規劃師" },
                { name: "橋樑與隧道設計師" },
                { name: "物流網路設計師" },
              ],
            },
            { name: "物流管理師" },
            { name: "供應鏈分析師" },
            { name: "倉儲與配送專家" },
          ],
        },
        {
          name: "學術研究領域",
          children: [
            { name: "行政人員" },
            { name: "學術研究員" },
            { name: "助理教授" },
            { name: "專利分析師" },
            { name: "教育科技研究員" },
          ],
        },
        {
          name: "創意設計產業",
          children: [
            { name: "多媒體開發人員" },
            { name: "遊戲設計工程師" },
            { name: "美術設計顧問" },
            { name: "影音剪輯師" },
            { name: "UI/UX 設計師" },
            { name: "視覺特效設計師" },
            { name: "品牌設計師" },
          ],
        },
      ],
    },
  };
},

  mounted() {
    this.renderTree(); // 在組件掛載後渲染樹狀圖
  },
  methods: {
    renderTree() {
      const svg = d3.select(this.$refs.treeSvg);
      const margin = { top: 10, right: 150, bottom: 20, left: 120 };
      const width = this.width - margin.left - margin.right;
      const height = this.height - margin.top - margin.bottom;

      // 設置SVG漸層背景
      svg
        .append("defs")
        .append("linearGradient")
        .attr("id", "gradient")
        .attr("x1", "0%")
        .attr("y1", "0%")
        .attr("x2", "0%")
        .attr("y2", "100%")
        .selectAll("stop")
        .data([
          { offset: "0%", color: "#3e065f" },
          { offset: "50%", color: "#240046" },
          { offset: "100%", color: "#000" },
        ])
        .enter()
        .append("stop")
        .attr("offset", d => d.offset)
        .attr("stop-color", d => d.color);

      svg
        .append("rect")
        .attr("width", this.width)
        .attr("height", this.height)
        .style("fill", "url(#gradient)");

      const g = svg
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      // 將數據轉換為樹狀結構
      const root = d3.hierarchy(this.treeData);
      const treeLayout = d3.tree().size([height, width]);
      treeLayout(root);

      // 繪製連接線
      g.selectAll(".link")
        .data(root.links())
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("d", d3
          .linkHorizontal()
          .x(d => d.y)
          .y(d => d.x))
        .style("fill", "none")
        .style("stroke", "#fff")
        .style("stroke-width", 2);

      // 繪製節點
      const nodes = g
        .selectAll(".node")
        .data(root.descendants())
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.y},${d.x})`);

      nodes
        .append("circle")
        .attr("r", 6)
        .style("fill", "#f8f9fa")
        .style("stroke", "#6610f2")
        .style("stroke-width", 2);

      nodes
        .append("text")
        .attr("dy", ".35em") // 垂直對齊
        .attr("x", d => (d.children ? 45 : 10)) // 根據是否有子節點調整文字位置
        .attr("y", d => (d.children ? -20 : 0)) // 根據是否有子節點調整文字位置
        .style("text-anchor", d => (d.children ? "end" : "start")) // 文字對齊方向
        .text(d => d.data.name)
        .style("font-size", "14px") /* 修改字體大小 */
        .style("font-family", "Arial, sans-serif") /* 修改字型 */
        .style("font-weight", "bold") /* 字體加粗 */
        .style("fill", "#f8f9fa") /* 修改字體顏色 */
        .style("letter-spacing", "1px"); /* 增加字間距 */

    },
  },
};
</script>

<style scoped>
/* 全局樣式 */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #3e065f;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #3e065f;
  color: white;
  padding: 0.5rem 1rem;
}

.title {
  font-size: 2rem;
  font-weight: bold;
}

.nav a {
  color: #fff;
  margin-left: 1rem;
  text-decoration: none;
  font-size: 1rem;
}

.nav a:hover {
  text-decoration: underline;
}

/* SVG 樹狀圖樣式 */
svg {
  display: block;
  margin: 0 auto;
  border-radius: 8px;
}

/* 卡片樣式 */
.card {
  margin: 20px auto; /* 下移卡片 */
  padding: 1.5rem;
  max-width: 1200px;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  color: #333;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 添加動畫效果 */
}

.card:hover {
  transform: translateY(-10px) scale(1.03); /* 滑鼠懸停時微微上移並放大 */
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3); /* 增加陰影強度 */
}

.card h2 {
  margin: 0 0 1rem;
  color: #6610f2;
}

.card p {
  font-size: 1rem;
  line-height: 1.5;
}
main {
  margin-top: 20px; /* 增加外層容器的上方間距，讓樹狀圖往下移 */
}

svg {
  display: block;
  margin: 0 auto;
  border-radius: 20px; /* 保持 SVG 的圓角 */
}

</style>

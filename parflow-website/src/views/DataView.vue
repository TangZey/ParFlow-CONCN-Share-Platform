<template>
  <div id="data-view">
    <h2 style="text-align: center; margin: 20px 0;">🌊 流域数据分享平台</h2>

    <!-- 搜索区域 -->
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="流域编号/名称">
          <el-input
            v-model="searchForm.keyword"
            placeholder="请输入编号或名称"
            clearable
            style="width: 220px;"
          />
        </el-form-item>
        <el-form-item label="所属地区">
          <el-select
            v-model="searchForm.region"
            placeholder="请选择地区"
            clearable
            style="width: 160px;"
          >
            <el-option label="长江流域" value="长江流域" />
            <el-option label="黄河流域" value="黄河流域" />
            <el-option label="淮河流域" value="淮河流域" />
            <el-option label="海河流域" value="海河流域" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>流域列表</span>
          <span style="font-size: 14px; color: #909399;">
            共 {{ tableData.length }} 条记录
          </span>
          <el-button type="primary" @click="handleDownload">下载数据</el-button>
        </div>
      </template>

      <el-table
        :data="tableData"
        border
        stripe
        style="width: 100%;"
        @selection-change="handleSelectionChange"
      >
        <!-- 手动复选框列，表头带“全选”文字 -->
        <el-table-column width="80" align="center">
          <template #header>
            <span style="display: flex; align-items: center; justify-content: center;">
              <el-checkbox :model-value="isAllSelected" @change="toggleAllSelection" />
              <span style="margin-left: 4px; font-weight: bold; font-size: 14px; color: #303133;">全选</span>
            </span>
          </template>
          <template #default="{ row }">
            <el-checkbox
              :model-value="isSelected(row)"
              @change="() => toggleRow(row)"
            />
          </template>
        </el-table-column>

        <el-table-column prop="id" label="编号" width="120" />
        <el-table-column prop="name" label="名称" width="150" />
        <el-table-column prop="region" label="所属地区" width="140" />
        <el-table-column prop="level" label="级别" width="100" />
        <el-table-column prop="description" label="基本信息" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" plain @click="viewDetail(scope.row)">
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 地图容器（占位） -->
    <el-card class="map-card" shadow="never">
      <template #header>
        <span>流域分布地图</span>
      </template>
      <div class="map-container" id="mapContainer">
        <div style="color: #bbb; text-align: center; line-height: 400px; user-select: none;">
          🗺️ 地图加载中 ...
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'DataView',
  data() {
    return {
      searchForm: {
        keyword: '',
        region: ''
      },
      tableData: [
        {
          id: 'WS001',
          name: '长江上游',
          region: '长江流域',
          level: '一级',
          description: '位于青藏高原至宜昌段，水资源丰富。'
        },
        {
          id: 'WS002',
          name: '黄河中游',
          region: '黄河流域',
          level: '二级',
          description: '流经黄土高原，泥沙含量大。'
        },
        {
          id: 'WS003',
          name: '淮河干流',
          region: '淮河流域',
          level: '一级',
          description: '介于长江与黄河之间，是重要的农业区。'
        }
      ],
      allData: [],
      selectedRows: []     // 存储当前选中的行（对象数组）
    };
  },
  computed: {
    // 是否全选
    isAllSelected() {
      if (this.tableData.length === 0) return false;
      return this.tableData.every(row => this.isSelected(row));
    }
  },
  mounted() {
    this.allData = [...this.tableData];
  },
  methods: {
    // 判断某一行是否被选中
    isSelected(row) {
      return this.selectedRows.some(item => item.id === row.id);
    },
    // 切换单行选中状态
    toggleRow(row) {
      const index = this.selectedRows.findIndex(item => item.id === row.id);
      if (index !== -1) {
        this.selectedRows.splice(index, 1);
      } else {
        this.selectedRows.push(row);
      }
    },
    // 切换全选
    toggleAllSelection(checked) {
      if (checked) {
        // 全选：将当前表格所有行加入 selectedRows（去重）
        const existingIds = new Set(this.selectedRows.map(r => r.id));
        this.tableData.forEach(row => {
          if (!existingIds.has(row.id)) {
            this.selectedRows.push(row);
          }
        });
      } else {
        // 取消全选：移除当前表格中所有行
        const currentIds = new Set(this.tableData.map(r => r.id));
        this.selectedRows = this.selectedRows.filter(r => !currentIds.has(r.id));
      }
    },
    // 搜索
    handleSearch() {
      const { keyword, region } = this.searchForm;
      let filtered = this.allData.filter(item => {
        let match = true;
        if (keyword) {
          const kw = keyword.trim().toLowerCase();
          match = match && (item.id.toLowerCase().includes(kw) || item.name.toLowerCase().includes(kw));
        }
        if (region) {
          match = match && item.region === region;
        }
        return match;
      });
      this.tableData = filtered;
      // 搜索后清空选中状态（因为当前选中可能不在过滤结果中）
      this.selectedRows = [];
    },
    // 重置搜索
    resetSearch() {
      this.searchForm.keyword = '';
      this.searchForm.region = '';
      this.tableData = [...this.allData];
      this.selectedRows = [];
    },
    // 查看详情
    viewDetail(row) {
      alert(`查看流域详情：${row.name}（编号：${row.id}）`);
    },
    // 下载按钮
    handleDownload() {
      if (this.selectedRows.length === 0) {
        alert('未选择流域，请先勾选需要下载的流域数据！');
        return;
      }
      const ids = this.selectedRows.map(r => r.id).join(', ');
      alert(`准备下载以下流域数据：${ids}\n（实际下载功能待对接后端实现）`);
    }
  }
};
</script>

<style scoped>
#data-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 40px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}
.search-card {
  margin-bottom: 20px;
}
.search-form {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}
.table-card {
  margin-bottom: 20px;
}
.map-card {
  margin-bottom: 20px;
}
.map-container {
  width: 100%;
  height: 400px;
  background-color: #f5f7fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed #dcdfe6;
}
</style>
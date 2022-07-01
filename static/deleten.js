function ddd(){
layui.use('table', function() {
           var table = layui.table;
console.log("111");

           var $ = layui.$, active = {
                   dnumber: function () { //获取选中数据
                   checkStatus = table.checkStatus('tid').data;
                   console.log(checkStatus);

               }
           };
       });}
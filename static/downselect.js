/*
function tableupdate(){
    //document.getElementById("demotable").innerHTML = "";
    layui.use('table', function(){
      $.ajax({
          url:'/../../tablecol',
          type:'POST',

          datatype:'JSON',
          data:{
              'entity':"classD"
          },
          success:function (data) {
          var data1 = JSON.parse(data);

          for(var i = 0; i< data1.length; i++){
              var d = data1[i];
              d = d['par'];
            // var c = JSON.stringify(d);
           //  console.log(typeof d);
         //    c = JSON.parse(c);

         //     d = JSON.stringify(d);
              var f = "<th lay-data='" + d + "'>" + data1[i]['name'] + "</th>";
              console.log(f);
             $("#col").append("<th lay-data='" + d + "'>" + data1[i]['name'] + "</th>");}

          }
    })

    });
}*/
function ta(){



    //document.getElementById("demotable").innerHTML = "";
    layui.use('table', function(){
      $.ajax({
          url:'/../../tablecol',
          type:'POST',

          data:{
              'doc':selectdoc,
              'sx':selectsx,
              //'entity':"classD"
          },
          success:function (data) {


          var data1 = JSON.parse(data);
          console.log(data1);
          var table = layui.table;
        //第一个实例

        //更新表格数据
        $.ajax({
             url: '/../../data',
                                  type : 'POST',

                                  data :{
                                      'doc':selectdoc,
                                      'sx':selectsx,

                                  },
                                  success: function (data) {
                                       // alert(data)
                                      table.render({
            elem: '#demotable'
            , height: 580
            ,checkbox: true
            , url: '../media/getdata/t' //数据接口

            , cols: [
                data1
            ]
            ,page: true
            ,limits:[10,20,30,50,100]
            ,limit: 10
            ,parseData:function (res) {
                                    var result;
                                    //console.log(this);
                                    //console.log(JSON.stringify(res));
                                    if (this.page.curr){
                                        result = res.data.slice(this.limit*(this.page.curr-1),this.limit*this.page.curr);
                                    }
                                    else {
                                        result = res.data.slice(0,this.limit);
                                    }
                                    return{
                                        "code":res.code,
                                        "mag":res.msg,
                                        "count":res.count,
                                        "data":result
                                    };
                                          }
            , toolbar: '#toolbarDemo'

        });
                                  },
                                  error: function (error) {
                                      alert('出错了，请稍后重试')
                                  },
        });

          table.on('toolbar(test)', function(obj){
  var checkStatus = table.checkStatus(obj.config.id);
  switch(obj.event){
    case 'add':
//<div class="layui-inline">
//     <label class="layui-form-label" style="width: 220px">类型</label>
//     <div class="layui-input-inline" style="width: 100px;">
//       <input type="text" name="typec" placeholder="" autocomplete="" class="layui-input">
//     </div>
        //根据当前所选图层动态生成添加页面
     /*   for(var i = 4; i< data1.length-1; i++) {
            console.log(data1[i]["field"]);
            var title = data1[i]['field'];

            document.getElementById("addd").innerHTML = '<div class="layui-inline"> <label class="layui-form-label" style="width: 220px">名称</label><div class="layui-input-inline" style="width: 100px;"><input type="text" name="aaa" autocomplete="必填" class="layui-input"></div></div>'
        }*/

        //添加增加按钮功能
      //console.log("add");

      layer.open({
          type: 2
          ,title:"添加数据" //不显示标题栏
                   // ,backgroundColor: '#ADD8E6'
           ,btn: ['关闭']
          ,btnAlign: 'c'
          ,area: ['70%','100%']
          ,shade: 0.8
          ,id: 'LAY_layuiadd' //设定一个id，防止重复弹出
                    ,anim:1
          ,moveType: 1 //拖拽模式，0或者1
          //,content: "tablea.html"
                   ,content: "adata.html"
          });

      //弹出提交表单
    break;
    case 'delete':
        layer.msg("删除");
      console.log('删除');

    break;
    case 'update':
      layer.msg('编辑');
    break;
  }
});
table.on('tool(test)', function(obj){ //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
  var data = obj.data; //获得当前行数据
  var layEvent = obj.event; //获得 lay-event 对应的值（也可以是表头的 event 参数对应的值）
  var tr = obj.tr; //获得当前行 tr 的 DOM 对象（如果有的话）

  if(layEvent === 'detail'){ //查看
    //do somehing
  } else if(layEvent === 'del'){ //删除
    layer.confirm('确定删除该行？', function(index){
      $.ajax({
          url:'/../../delete',
          type :'POST',
          data:{
              entity: "classD",
              id: data.id,
              leixing: data.leixing
          },
          success:function (data) {
              console.log(data)
          },
           error: function (error) {
              alert('出错了，请稍后重试')
           },

      }) ;
      obj.del(); //删除对应行（tr）的DOM结构，并更新缓存
      layer.close(index);
      //向服务端发送删除指令
    });
  } else if(layEvent === 'edit'){ //编辑
    //do something
     //layer.msg("edit");
    //同步更新缓存对应的值


//
      console.log("comein");
      layer.open({
          type: 2
          ,title: '编辑信息'
          ,content: 'edit.html' //展示test1.html中的layui表单
          ,maxmin: true   //允许最大化
          ,area: ['70%', '100%']   //弹窗的大小

          ,btn: ['确定', '取消']
          //yes函数是点击弹窗后回调的函数
          ,yes: function(index, layero){
              //通过以下的方法获取回调的数值

            /*  for(var i=0;i<data1.length-1;i++){

                  console.log(data1[i]);
                  //var a = $(layero).find('iframe')[0].contentWindow. + data1[i] + .value;
              }*/

             console.log("really?");

              var newid = $(layero).find('iframe')[0].contentWindow.id.value;
              var newleixing = $(layero).find('iframe')[0].contentWindow.leixing.value;
              var newcoding = $(layero).find('iframe')[0].contentWindow.coding.value;
              var newname = $(layero).find('iframe')[0].contentWindow.names.value;
              var newtypec = $(layero).find('iframe')[0].contentWindow.typec.value;
              var newnode = $(layero).find('iframe')[0].contentWindow.node.value;
              var newlevel = $(layero).find('iframe')[0].contentWindow.level.value;
              var newwidth= $(layero).find('iframe')[0].contentWindow.width.value;
              var newpwidth = $(layero).find('iframe')[0].contentWindow.pwidth.value;
              var newblength = $(layero).find('iframe')[0].contentWindow.blength.value;
              var newjklength = $(layero).find('iframe')[0].contentWindow.jklength.value;
              var newton = $(layero).find('iframe')[0].contentWindow.ton.value;
              var newkilo = $(layero).find('iframe')[0].contentWindow.kilo.value;
              var newbigao = $(layero).find('iframe')[0].contentWindow.bigao.value;
              var newcmonth = $(layero).find('iframe')[0].contentWindow.cmonth.value;
              var newwdeep = $(layero).find('iframe')[0].contentWindow.wdeep.value;
              var newdizhi = $(layero).find('iframe')[0].contentWindow.dizhi.value;
              var newminbj = $(layero).find('iframe')[0].contentWindow.minbj.value;
              var newmaxzb = $(layero).find('iframe')[0].contentWindow.maxzb.value;
              var newspec = $(layero).find('iframe')[0].contentWindow.spec.value;
              var newzjzz = $(layero).find('iframe')[0].contentWindow.zjzz.value;
              var newwgbzz = $(layero).find('iframe')[0].contentWindow.wgbzz.value;

                  //同步数据表格中的数据
                  obj.update({

                      id:newid,
                      leixing:newleixing,
                      coding:newcoding,
                      name:newname,
                      typec:newtypec,
                      node:newnode,
                      level:newlevel,
                      width:newwidth,
                      pwidth:newpwidth,
                      blength:newblength,
                      jklength:newjklength,
                      ton:newton,
                      kilo:newkilo,
                      bigao:newbigao,
                      cmonth:newcmonth,
                      wdeep:newwdeep,
                      dizhi:newdizhi,
                      minbj:newminbj,
                      maxzb:newmaxzb,
                      spec:newspec,
                      zjzz:newzjzz,
                      wgbzz:newwgbzz,



              });
              //利用ajax同步数据库的数据
                    $.ajax({
                                       url:'/../../update',
                                       type:"POST",
                                      // contentType:"application/json;charset=utf-8",
                                      // dataType:'json',
                                       data:{
                                           currentid:data.id,
                                           currentleixing:data.leixing,
                                           id:newid,
                                           leixing:newleixing,
                                           coding:newcoding,
                                           name:newname,
                                           typec:newtypec,
                                           node:newnode,
                                           level:newlevel,
                                           width:newwidth,
                                           pwidth:newpwidth,
                                           blength:newblength,
                                           jklength:newjklength,
                                           ton:newton,
                                           kilo:newkilo,
                                           bigao:newbigao,
                                           cmonth:newcmonth,
                                           wdeep:newwdeep,
                                           dizhi:newdizhi,
                                           minbj:newminbj,
                                           maxzb:newmaxzb,
                                           spec:newspec,
                                           zjzz:newzjzz,
                                           wgbzz:newwgbzz,
                                       },
                                       success:function(data){
                                           layer.msg('操作成功');

                                           console.log(data)
                                       },
                                       error:function(error){
                                         layer.msg('操作失败，稍后再试！');
                                       }
                                   });


              layer.close(index);

              }
              ,success: function(layero, index){


              //获取当前数据
              var div = layero.find('iframe').contents().find('#useradmin');  // div.html() div里面的内容,不包含当前这个div
              var body = layer.getChildFrame('body', index);  // body.html() body里面的内容
              var iframeWindow = window['layui-layer-iframe'+ index];   //得到iframe页的窗口对象
              //通过test1.html中各个输入框的id可以进行赋值
              body.find("#id").val(data.id);
              body.find("#leixing").val(data.leixing);
              body.find("#coding").val(data.coding);
              body.find("#names").val(data.name);
              body.find("#typec").val(data.typec);
              body.find("#node").val(data.node);
              body.find("#level").val(data.level);
              body.find("#width").val(data.width);
              body.find("#pwidth").val(data.pwidth);
              body.find("#blength").val(data.blength);
              body.find("#jklength").val(data.jklength);
              body.find("#ton").val(data.ton);
              body.find("#kilo").val(data.kilo);
              body.find("#bigao").val(data.bigao);
              body.find("#cmonth").val(data.cmonth);
              body.find("#wdeep").val(data.wdeep);
              body.find("#dizhi").val(data.dizhi);
              body.find("#minbj").val(data.minbj);
              body.find("#maxzb").val(data.maxzb);
              body.find("#spec").val(data.spec);
              body.find("#zjzz").val(data.zjzz);
              body.find("#wgbzz").val(data.wgbzz);


                                }
                            });









/*
    obj.update({
      username: '123'
      ,title: 'xxx'
    });*/


  } else if(layEvent === 'LAYTABLE_TIPS'){
    //layer.alert('Hi，头部工具栏扩展的右侧图标。');
  }
});


          }
    });
//         table.render({
//   elem: '#demotable'
//   ,toolbar: '#toolbarDemo'
//   //,…… //其他参数
// });

//触发事件
// table.on('toolbar(test)', function(obj){
//   var checkStatus = table.checkStatus(obj.config.id);
//   switch(obj.event){
//     case 'add':
//       layer.msg('添加');
//     break;
//     case 'delete':
//       layer.msg('删除');
//     break;
//     case 'update':
//       layer.msg('编辑');
//     break;
//   }
// });

    });
}
var script=document.createElement("script");
script.type="text/javascript";
script.src="/js/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(script);
setTimeout(function(){
$(document).ready(function(){
$('#rolemanager').click(function(){
	$(".all_over").css("display","block");
	$(".role").css("display","block");
	$.ajax({url:'/addrole/',
		type:'get',
		dataType:'json',
		success:function(data){
			var html='';
			$.each(data,function(i,item){
				var dataObj=eval("("+item+")");
				html+='<tr id="roleinfo"><td width="200px;" id="rolename" align="center">'+dataObj.name+'</td><td width="200px" align="center">'+dataObj.description+'</td><td width="200px;" align="center" id="status">****</td><td width="200px;">'+dataObj.updatetime+'</td><td width="200px;"><img id="edit_role" width="10%" src="/js/edit.jpg"><span id="editbutton" style="display:none;cursor:pointer;">编辑角色</span>&nbsp;<img id="delete_role" width="11%" src="/js/delete.png"><span id="deletebutton" style="display:none;cursor:pointer;">删除角色</span></td></tr>'
			});
			var head='<tr style="background-color:gray;"><td width="200px;" align="center">角色名称</td><td width="200px" align="center">角色描述</td><td width="200px;" align="center">所属用户</td><td width="200px;">创建时间</td><td width="200px;">操作</td></tr>';
			$('#rolelist').html(head+html);
			
		}
	});
});
$(".button_addrole").click(function(){
	var tooltip="<div class='little_over'></div><div id='addrole' class='addrole'><font size='5px;' color='blue;'><span>新增角色</span></font><hr/><table><tr><td><label for='rolename'>角色名称:</lable></td><td><input type='text' placeholder='角色名称' id='rolename'  style='width:200px;height:25px' required></td></tr><tr><td><label for='rolename'>角色描述:</lable></td><td><input type='text' placeholder='描述信息' id='roledesc' style='width:200px;height:25px;' size='25' required></td></tr><tr><td><input type='button' id='confirm' value='确定'></td><td><input id='cancle' type='button' value='取消'></td></tr></table><div class='close1'><span style='font-size:16px;cursor:default;font-weight:bold'><img src='/js/timg.jpg/' alt='关闭' height='20px'></span></div></div>";
	$('body').append(tooltip);
	$(".little_over").show();
	$(".addrole").show();
	$(".addrole .close1").show();

	$('#addrole').find("#confirm").attr('disabled','true');
	$("#addrole").find("#rolename").on('input',function(){
		var rolename=$('#addrole').find("#rolename").val();
		var roledesc=$('#addrole').find("#roledesc").val();
		if(rolename!=''&&roledesc!=''){
			$('#addrole').find("#confirm").removeAttr('disabled');
		}else{
			$('#addrole').find("#confirm").attr('disabled','true');
		}
	});
	$("#addrole").find("#roledesc").on('input',function(){
		var rolename=$('#addrole').find("#rolename").val();
		var roledesc=$('#addrole').find("#roledesc").val();
		if(rolename!=''&&roledesc!=''){
			$('#addrole').find("#confirm").removeAttr('disabled');
		}else{
			$('#addrole').find("#confirm").attr('disabled','true');
		}
	});
	$("#addrole").find("#confirm").click(function(){
		var rolename=$('#addrole').find("#rolename").val();
                var roledesc=$('#addrole').find("#roledesc").val();
		$.ajax({url:'/addrole/',
			type:'post',
			dataType:'json',
			data:{rolename:rolename,roledesc:roledesc,action:'1'},
			success:function(data){
				if(data==4){
					alert("角色已经存在");
					$('#addrole').find("#confirm").attr("disabled","true")
					$('#addrole').find('#rolename').val('');
					$('#addrole').find('#rolename').focus();
				}else{
				var tooltip=$(".little_over");
				tooltip.remove();
				var tooltip=$("#addrole");
				tooltip.remove();
				var html='';
				$.each(data,function(i,item){
					var dataObj=eval("("+item+")");
					html+='<tr id="roleinfo"><td width="200px;" id="rolename" align="center">'+dataObj.name+'</td><td width="200px" align="center">'+dataObj.description+'</td><td width="200px;" align="center" id="status">****</td><td width="200px;">'+dataObj.updatetime+'</td><td width="200px;"><img id="edit_role" width="10%" src="/js/edit.jpg"><span id="editbutton" style="display:none;cursor:pointer;">编辑用户</span>&nbsp;<img id="delete_role" width="11%" src="/js/delete.png"><span id="deletebutton" style="display:none;cursor:pointer;">删除用户</span></td></tr>'
				});
				var head='<tr style="background-color:gray;"><td width="200px;" align="center">角色名称</td><td width="200px" align="center">角色描述</td><td width="200px;" align="center">所属用户</td><td width="200px;">创建时间</td><td width="200px;">操作</td></tr>';
				$('#rolelist').html(head+html);
			
				}
				
			}
		})	
	});
	$("#addrole").find("#cancle").click(function(){
		var tooltip=$(".little_over");
                tooltip.remove();
                var tooltip=$("#addrole");
                tooltip.remove();
	});
	$("#addrole").find(".close1").click(function(){
		var tooltip=$(".little_over");
                tooltip.remove();
                var tooltip=$("#addrole");
                tooltip.remove();
	});
});

$(".button_addrole").mouseover(function(){
	$(this).css("border","1px solid lightblue");
}).mouseout(function(){
	$(this).css("border","1px solid black");
});

$(".button_editrole").click(function(){
	var rolename=$("#rolelist").find(".tablecolor").children("td:eq(0)");
	var roledesc=$("#rolelist").find(".tablecolor").children("td:eq(1)");
	if(rolename.text()!='系统管理员' &&rolename.length>0){
	var tooltip="<div class='little_over'></div><div id='editrole' class='editrole'><font size='5px;' color='lightblue;'>角色编辑</font><hr/><font size='5px;'>角色名称:&nbsp;&nbsp;<input type='text' id='rolename' style='height:25px;' value="+rolename.text()+"></br></font></br><font size='5px;'>角色描述:<input type='text' style='height:25px;'id='roledesc' value="+$.trim(roledesc.text())+">"+"</br></br><input type='button' value='确定' id='confirm'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type='button' value='取消' id='cancle'><div class='close1'><span style='font-size:16px;cursor:default;font-weight:bold'><img src='/js/timg.jpg/' alt='关闭' height='20px'></span></div><input type='hidden' id='hid_rolename' style='height:25px;' value="+rolename.text()+"></div>";
        $('body').append(tooltip);
        $(".little_over").show();
       	$(".editrole").css("display","block");
        $(".editrole .close1").css("display","block");

	 $(document).ready(function(){
                        $(".editrole").find("#confirm").attr("disabled","true");
                });

	$(".editrole #rolename").on('input',function(e){
		var rolename=$(".editrole").find("#rolename").val();
		var roledesc= $(".editrole").find("#roledesc").val();
		if(rolename!='' && roledesc!=''){
			  $(".editrole").find("#confirm").removeAttr('disabled');
		}else{
			  $(".editrole").find("#confirm").attr('disabled',"true");
		}
	});
	$(".editrole #roledesc").on('input',function(){
		var rolename=$(".editrole #rolename");
		var roledesc= $(".editrole #roledesc");
		if(rolename.val()!='' && roledesc.val()!=''){
			  $(".editrole").find("#confirm").removeAttr('disabled');
		}else{
			  $(".editrole").find("#confirm").attr('disabled',"true");
		}
	});
	$("#editrole").find("#confirm").click(function(){
		var newrolename=$('#editrole').find("#rolename").val();
		var rolename=$("#editrole").find("#hid_rolename").val();
                var roledesc=$('#editrole').find("#roledesc").val();
		if (newrolename==rolename){
			newval='';
		}else{
			newval=newrolename;
		}
		$.ajax({url:'/addrole/',
			type:'post',
			dataType:'json',
			data:{rolename:rolename,newrolename:newval,roledesc:roledesc,action:'2'},
			success:function(data){
				if(data==4){
					alert("其他角色已经存在");
					$('#editrole').find("#confirm").attr("disabled","true")
					$('#editrole').find('#rolename').val('');
					$('#editrole').find('#rolename').focus();
				}else{
				var tooltip=$(".little_over");
				tooltip.remove();
				var tooltip=$("#editrole");
				tooltip.remove();
				var html='';
				$.each(data,function(i,item){
					var dataObj=eval("("+item+")");
					html+='<tr id="roleinfo"><td width="200px;" id="rolename" align="center">'+dataObj.name+'</td><td width="200px" align="center">'+dataObj.description+'</td><td width="200px;" align="center" id="status">****</td><td width="200px;">'+dataObj.updatetime+'</td><td width="200px;"><img id="edit_role" width="10%" src="/js/edit.jpg"><span id="editbutton" style="display:none;cursor:pointer;">编辑用户</span>&nbsp;<img id="delete_role" width="11%" src="/js/delete.png"><span id="deletebutton" style="display:none;cursor:pointer;">删除用户</span></td></tr>'
				});
				var head='<tr style="background-color:gray;"><td width="200px;" align="center">角色名称</td><td width="200px" align="center">角色描述</td><td width="200px;" align="center">所属用户</td><td width="200px;">创建时间</td><td width="200px;">操作</td></tr>';
				$('#rolelist').html(head+html);
			
				}
				
			}
		})	
	});
	$("#editrole").find("#cancle").click(function(){
		var tooltip=$('.little_over');
		tooltip.remove();
		var tooltip=$('.editrole');
		tooltip.remove();
	});
	$("#editrole .close1").click(function(){
		var tooltip=$('.little_over');
		tooltip.remove();
		var tooltip=$('.editrole');
		tooltip.remove();
	});
	}else if(rolename.text()=='系统管理员'){
			alert("管理员不能编辑");
		
	}else{
		alert("必须选择一条记录!");
	}


});


$(".button_editrole").mouseover(function(){
	$(this).css("border","1px solid lightblue");
}).mouseout(function(){
	$(this).css("border","1px solid black");
});

$(".deleterole").click(function(){
		var rolename=$("#rolelist").find(".tablecolor").children("td:eq(0)");
		if(rolename.text()!='系统管理员'&&rolename.length>0){
                var tooltip="<div class='little_over'></div><div id='deleterole' style='position:absolute;top:20%;left:50%;width:600px;height:100px;background:gray;border:1px solid lightblue;z-index:1007;'>角色删除<hr/><font color='blue' size='5px'>您是否要删除角色"+rolename.text()+"?</font><div id='confirm' style='position:absolute;top:80px;left:25%;background:lightblue;height:20px;width:55px;'><span style='cursor:pointer;'>确定</span></div><div id='cancle' style='position:absolute;top:80px;left:55%;background:lightblue;height:20px;width:55px;'><span  style='cursor:pointer;'>取消</span></div><input type='hidden'></div>";
                 $('body').append(tooltip);
                $(".little_over").css('display','block');
                var _move=false;
                $("#deleterole").mousedown(function(e){
                        _move=true;
                        _x=e.pageX-parseInt($("#deleterole").css("left"));
                        _y=e.pageY-parseInt($("#deleterole").css("top"));
                        $("#deleterole").fadeTo(20,0.5);
                }).mousemove(function(e){
                        if(_move){
                                var x=e.pageX-_x;
                                var y=e.pageY-_y;
                                $("#deleterole").css({top:y,left:x});
                        }
                }).mouseup(function(e){
                        _move=false;
                        $("#deleterole").fadeTo(1);
                });
		

		$("#deleterole").find("#cancle").click(function(){
			var tooltip=$(".little_over");
			tooltip.remove();
			var tooltip=$("#deleterole");
			tooltip.remove();
		});		
		


		$("#deleterole").find("#confirm").click(function(){
                $.ajax({url:'/addrole/',
                        type:'post',
                        data:{rolename:rolename.text(),action:'3'},
			dataType:'json',
                        success:function(data){
                                var tooltip=$(".little_over");
                                tooltip.remove();
                                var tooltip=$("#deleterole");
                                tooltip.remove();
                                var html='';
                                $.each(data,function(i,item){
                                        var dataObj=eval("("+item+")");
                                        html+='<tr id="roleinfo"><td width="200px;" id="rolename" align="center">'+dataObj.name+'</td><td width="200px" align="center">'+dataObj.description+'</td><td width="200px;" align="center" id="status">****</td><td width="200px;">'+dataObj.updatetime+'</td><td width="200px;"><img id="edit_role" width="10%" src="/js/edit.jpg"><span id="editbutton" style="display:none;cursor:pointer;">编辑用户</span>&nbsp;<img id="delete_role" width="11%" src="/js/delete.png"><span id="deletebutton" style="display:none;cursor:pointer;">删除用户</span></td></tr>';
                                });
                                var head='<tr style="background-color:gray;"><td width="200px;" align="center">角色名称</td><td width="200px" align="center">角色描述</td><td width="200px;" align="center">所属用户</td><td width="200px;">创建时间</td><td width="200px;">操作</td></tr>';
                                $('#rolelist').html(head+html);
                                }

                        })
        	});
	
		}else if(rolename.text()=='系统管理员'){
			alert("管理员不能删除");
		}else{
			alert("必须选择一条记录");
		}
                       

});





$(".deleterole").mouseover(function(){
        $(this).css("border","1px solid lightblue");
}).mouseout(function(){
        $(this).css("border","1px solid black");
});

});

},
				$(this).on("click","#roleinfo",function(e){
					$(this).addClass("tablecolor").siblings("#roleinfo").removeClass("tablecolor");
					var name=$(this).find("td:eq(0)");
				}),
				$(this).on("hover","#roleinfo",function(e){
					$(this).addClass("trcolor").siblings("#roleinfo").removeClass("trcolor");
					var name=$(this).find("td:eq(0)");
				}),function(){
					$(this).removeClass("tablecolor");
				},

				$(this).on("hover","#edit_role",function(e){
					 $(this).css("width","12%");
                        		 $(this).next().show();
				}),function(){
					$(this).css("width","10%");
                        		$(this).next().hide();
				},
				$(this).on("hover","#delete_role",function(e){
					 $(this).css("width","12%");
                        		 $(this).next().show();
				}),function(){
					$(this).css("width","10%");
                        		$(this).next().hide();
				},
				$(this).on("click","#delete_role",function(e){
					var rolename=$(this).parent().parent().children("td:eq(0)");
					if(rolename.text()!='系统管理员' && rolename.length>0){
                			var tooltip="<div class='little_over'></div><div id='deleterole' style='position:absolute;top:20%;left:50%;width:600px;height:100px;background:gray;border:1px solid lightblue;z-index:1007;'>角色删除<hr/><font color='blue' size='5px'>您是否要删除角色"+rolename.text()+"?</font><div id='confirm' style='position:absolute;top:80px;left:25%;background:lightblue;height:20px;width:55px;'><span style='cursor:pointer;'>确定</span></div><div id='cancle' style='position:absolute;top:80px;left:55%;background:lightblue;height:20px;width:55px;'><span  style='cursor:pointer;'>取消</span></div><input type='hidden'></div>";
                 			$('body').append(tooltip);
                			$(".little_over").css('display','block');
               			        var _move=false;
                			$("#deleterole").mousedown(function(e){
                      			 _move=true;
                        		_x=e.pageX-parseInt($("#deleterole").css("left"));
                      			  _y=e.pageY-parseInt($("#deleterole").css("top"));
                       			 $("#deleterole").fadeTo(20,0.5);
                			}).mousemove(function(e){
                      				 if(_move){
                                			var x=e.pageX-_x;
                                			var y=e.pageY-_y;
                                			$("#deleterole").css({top:y,left:x});
                        		}
               				 }).mouseup(function(e){
                       				 _move=false;
                      				  $("#deleterole").fadeTo(1);
               				 });
				$("#deleterole").find("#cancle").click(function(){
					var tooltip=$(".little_over");
					tooltip.remove();
					var tooltip=$("#deleterole");
					tooltip.remove();
				});

				$("#deleterole").find("#confirm").click(function(){
                			$.ajax({url:'/addrole/',
                        			type:'post',
                        			data:{rolename:rolename.text(),action:'3'},
						dataType:'json',
                        			success:function(data){
                               			 var tooltip=$(".little_over");
                                		tooltip.remove();
                                		var tooltip=$("#deleterole");
                              			  tooltip.remove();
                                		var html='';
                               			 $.each(data,function(i,item){
                                        	var dataObj=eval("("+item+")");
                                     		   html+='<tr id="roleinfo"><td width="200px;" id="rolename" align="center">'+dataObj.name+'</td><td width="200px" align="center">'+dataObj.description+'</td><td width="200px;" align="center" id="status">****</td><td width="200px;">'+dataObj.updatetime+'</td><td width="200px;"><img id="edit_role" width="10%" src="/js/edit.jpg"><span id="editbutton" style="display:none;cursor:pointer;">编辑用户</span>&nbsp;<img id="delete_role" width="11%" src="/js/delete.png"><span id="deletebutton" style="display:none;cursor:pointer;">删除用户</span></td></tr>';
                               			 });
                               			 var head='<tr style="background-color:gray;"><td width="200px;" align="center">角色名称</td><td width="200px" align="center">角色描述</td><td width="200px;" align="center">所属用户</td><td width="200px;">创建时间</td><td width="200px;">操作</td></tr>';
                                		$('#rolelist').html(head+html);
                                	}

                        	})
        			});		
		
					
		
				}else if(rolename.text()=='系统管理员'){
					alert("管理员不能删除");
				}	




				}),
				$(this).on("click","#edit_role",function(e){
					var rolename=$(this).parent().parent().children("td:eq(0)");
					if(rolename.text()!='系统管理员'){
        				var roledesc=$(this).parent().parent().children("td:eq(1)");
        				var tooltip="<div class='little_over'></div><div id='editrole' class='editrole'><font size='5px;' color='lightblue;'>角色编辑</font><hr/><font size='5px;'>角色名称:&nbsp;&nbsp;<input type='text' id='rolename' style='height:25px;' value="+rolename.text()+"></br></font></br><font size='5px;'>角色描述:<input type='text' style='height:25px;'id='roledesc' value="+$.trim(roledesc.text())+">"+"</br></br><input type='button' value='确定' id='confirm'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type='button' value='取消' id='cancle'><div class='close1'><span style='font-size:16px;cursor:default;font-weight:bold'><img src='/js/timg.jpg/' alt='关闭' height='20px'></span></div><input type='hidden' id='hid_rolename' style='height:25px;' value="+rolename.text()+"></div>";
        				$('body').append(tooltip);
        				$(".little_over").show();
        				$(".editrole").css("display","block");
       					 $(".editrole .close1").css("display","block");
		
  				       $(document).ready(function(){
                       			 $(".editrole").find("#confirm").attr("disabled","true");
               				 });

   					$(".editrole #rolename").on('input',function(e){
                				var rolename=$(".editrole").find("#rolename").val();
                				var roledesc= $(".editrole").find("#roledesc").val();
                				if(rolename!='' && roledesc!=''){
                          				$(".editrole").find("#confirm").removeAttr('disabled');
               				 	}else{
                          				$(".editrole").find("#confirm").attr('disabled',"true");
               				 	}
    					});
   					$(".editrole #roledesc").on('input',function(e){
                				var rolename=$(".editrole").find("#rolename").val();
                				var roledesc= $(".editrole").find("#roledesc").val();
                				if(rolename!='' && roledesc!=''){
                          				$(".editrole").find("#confirm").removeAttr('disabled');
               				 	}else{
                          				$(".editrole").find("#confirm").attr('disabled',"true");
               				 	}
    					});
					$("#editrole").find("#confirm").click(function(){
                				var newrolename=$('#editrole').find("#rolename").val();
               				 	var rolename=$("#editrole").find("#hid_rolename").val();
                				var roledesc=$('#editrole').find("#roledesc").val();
               				 	if (newrolename==rolename){
                        				newval='';
               				 	}else{
                       			 		newval=newrolename;
                				}
                				$.ajax({url:'/addrole/',
                        			type:'post',
                        			dataType:'json',
                        			data:{rolename:rolename,newrolename:newval,roledesc:roledesc,action:'2'},
                       			 	success:function(data){
                                		if(data==4){
                                       			 alert("其他角色已经存在");
                                       		 	$('#editrole').find("#confirm").attr("disabled","true")
                                      		  	$('#editrole').find('#rolename').val('');
                                        		$('#editrole').find('#rolename').focus();
                                		}else{
                                			var tooltip=$(".little_over");
                                			tooltip.remove();
                                			var tooltip=$("#editrole");
                               			 	tooltip.remove();
                                			var html='';
                                			$.each(data,function(i,item){
                                        		var dataObj=eval("("+item+")");
                                       			 html+='<tr id="roleinfo"><td width="200px;" id="rolename" align="center">'+dataObj.name+'</td><td width="200px" align="center">'+dataObj.description+'</td><td width="200px;" align="center" id="status">****</td><td width="200px;">'+dataObj.updatetime+'</td><td width="200px;"><img id="edit_role" width="10%" src="/js/edit.jpg"><span id="editbutton" style="display:none;cursor:pointer;">编辑角色</span>&nbsp;<img id="delete" width="11%" src="/js/delete.png"><span id="deletebutton" style="display:none;cursor:pointer;">删除角色</span></td></tr>'
                                			});
                                			var head='<tr style="background-color:gray;"><td width="200px;" align="center">角色名称</td><td width="200px" align="center">角色描述</td><td width="200px;" align="center">所属用户</td><td width="200px;">创建时间</td><td width="200px;">操作</td></tr>';
                              			  	$('#rolelist').html(head+html);

                                	}

                        	}		
                		})
       				 });


				$("#editrole").find("#cancle").click(function(){
					var tooltip=$(".little_over");
                                        tooltip.remove();
                                        var tooltip=$("#editrole");
                                        tooltip.remove();
				});
				$("#editrole").find(".close1").click(function(){
					var tooltip=$(".little_over");
                                        tooltip.remove();
                                        var tooltip=$("#editrole");
                                        tooltip.remove();
				});}else if(rolename.text()=='系统管理员'){
					alert("系统管理员不能编辑");
				}
				}),



				


				


100);



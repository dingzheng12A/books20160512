var script=document.createElement("script");
script.type="text/javascript";
script.src="/js/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(script);
setTimeout(function(){
	$('#permanager').click(function(){
		$(".all_over").css('display','block');
		$('.perm').css('display','block');
		$('.perm .close1').css('display','block');

		$(".perm .button_addperm").mouseover(function(){
			$(this).css('border',"1px solid lightblue");
		}).mouseout(function(){
			$(this).css('border','1px solid black');
		});
		$.ajax({url:'/permlist/',
			type:'get',
			dataType:'json',
			success:function(data){
				var html='';
				$.each(data,function(index,item){
					var dataObj=eval("("+item+")");
					html+='<tr id="perminfo"><td width="200px;" align="center">'+dataObj.name+'</td><td width="200px" align="center">'+dataObj.codename+'</td><td width="200px" align="center">'+dataObj.content+'</td><td width="200px;">操作</td></tr>';
				});
				var head='<tr style="background-color:gray"><td width="200px;" align="center">权限名称</td><td width="200px" align="center">权限描述</td><td width="200px" align="center">应用目标</td><td width="200px;">操作</td></tr>';
				$('#permlist').html(head+html);
			}
		})
		$('.perm .close1').click(function(){
			$(".all_over").css('display','none');
                	$('.perm').css('display','none');
                	$('.perm .close1').css('display','none');
		});

		
		$('.perm .button_addperm').click(function(){
			var tooltip='<div class="little_over"></div><div class="addperm"><div style="float:left;">增加权限</div><hr/></br><div style="float:left;text-align:left;"><font size="3px;">权限名称:</font><input type="text" id="permname"/></br></br><font size="3px;">权限内容:</font><input type="text" style="width:200px;" id="content"/></br></br></br></br></br><input id="confirm" type="button" value="确定">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="cancle" type="button" value="取消"></div></div>';
			$('body').append(tooltip);
			$('.little_over').show();

			$(document).ready(function(){
				$(".addperm").find("#confirm").attr("disabled","true");
			});

			$(".addperm #permname").on("input",function(){
				var permname=$(".addperm").find("#permname").val();
                                var content=$(".addperm").find("#content").val();
				if(permname!=''&&content!=''){
					$(".addperm").find("#confirm").removeAttr("disabled");
				}else{
					$(".addperm").find("#confirm").attr("disabled","true");
				}
			});
			$(".addperm #content").on("input",function(){
				var permname=$(".addperm").find("#permname").val();
                                var content=$(".addperm").find("#content").val();
				if(permname!=''&&content!=''){
					$(".addperm").find("#confirm").removeAttr("disabled");
				}else{
					$(".addperm").find("#confirm").attr("disabled","true");
				}
			});


			$(".addperm").find("#confirm").click(function(){
				var permname=$(".addperm").find("#permname").val();
				var content=$(".addperm").find("#content").val();
				$.ajax({url:'/addperm/',
					type:'post',
					data:{permname:permname,content:content},
					dataType:'json',
					 success:function(data){
                                	var html='';
					var tooltip=$('.little_over');
                                	tooltip.remove();
                                	var tooltip=$(".addperm");
                                	tooltip.remove();
                                	$.each(data,function(index,item){
                                        	var dataObj=eval("("+item+")");
                                        	html+='<tr id="perminfo"><td width="200px;" align="center">'+dataObj.name+'</td><td width="200px" align="center">'+dataObj.codename+'</td><td width="200px" align="center">'+dataObj.content+'</td><td width="200px;">操作</td></tr>';
                                	});
                                	var head='<tr style="background-color:gray"><td width="200px;" align="center">权限名称</td><td width="200px" align="center">权限描述</td><td width="200px" align="center">应用目标</td><td width="200px;">操作</td></tr>';
                                	$('#permlist').html(head+html);
                        		}
				});
			});

			$(".addperm").find("#cancle").click(function(){
				var tooltip=$('.little_over');
				tooltip.remove();
				var tooltip=$(".addperm");
				tooltip.remove();
			});
		});


		

	});
},
		 $(this).on("click","#perminfo",function(e){
                                        $(this).addClass("tablecolor").siblings("#perminfo").removeClass("tablecolor");
                                        var name=$(this).find("td:eq(0)");
                                }),
                                $(this).on("hover","#perminfo",function(e){
                                        $(this).addClass("trcolor").siblings("#perminfo").removeClass("trcolor");
                                        var name=$(this).find("td:eq(0)");
                                }),function(){
                                        $(this).removeClass("tablecolor");
                                },
100);



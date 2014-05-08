/**
	author comger@gmail.com
	全局方法
**/

function select_nav(classname){
	$('#nav-list li').removeClass('open').removeClass('active');
	$('#nav-list li li').removeClass('active');

	var nav = $('#nav-list').find('.'+classname);
	nav.addClass('active');
	nav.parents('.submenu').show();
	nav.parents('#nav-list li').addClass('open');
}

$(function(){
	var editor;
	KindEditor.ready(function(K) {
		editor = K.create('textarea.KindEditor', {
			resizeType : 1,
			allowPreviewEmoticons: false,
			allowImageUpload: true,
			allowFileManager: true,
			fileManagerJson: '/admin/files/image/?format=json&limit=100',
			uploadJson: '/admin/file/upload',

			items : [
				'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
				'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
				'insertunorderedlist', '|', 'emoticons', 'image', 'insertfile' , 'baidumap', 'link', '|', 'template','code','quickformat','clearhtml','|','source','fullscreen']
		});
	});
	
})
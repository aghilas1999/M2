
/**
 * Atto HTML editor
 *
 * @package    atto_reciteditor
 * @copyright  2019 RECIT
 * @license    {@link http://www.gnu.org/licenses/gpl-3.0.html} GNU GPL v3 or later
 */
M=M||{};M.recit=M.recit||{};M.recit.reciteditor=M.recit.reciteditor||{};M.recit.reciteditor.settings={currentthemesubrev:1}
M.recit.reciteditor.Popup=class{constructor(content){let modal=document.createElement('div');modal.classList.add('modal','fade','attoreciteditor_popup');let inner2=document.createElement('div');inner2.classList.add('modal-dialog');modal.appendChild(inner2);let inner=document.createElement('div');inner.classList.add('modal-content');inner2.appendChild(inner);let header=document.createElement('div');header.classList.add('modal-header');inner.appendChild(header);let btn=document.createElement('button');btn.classList.add('close');btn.innerHTML='<span aria-hidden="true">&times;</span>';btn.setAttribute('data-dismiss','modal');header.appendChild(btn);let body=document.createElement('div');body.classList.add('modal-body');inner.appendChild(body);body.appendChild(content);document.body.appendChild(modal);this.popup=modal;$(modal).modal({show:!0,backdrop:!0});let that=this;$(".modal-backdrop").click(()=>$(this.popup).modal('hide'));$(modal).on('hidden.bs.modal',function(e){that.destroy()})}
destroy(){this.popup.remove()}
update(){$(this.popup).modal('handleUpdate')}}
M.recit.reciteditor.init_settings=function(_,settings){M.recit.reciteditor.settings=settings}
document.body.addEventListener('click',function(e){if(e.target&&e.target.classList.contains('attoreciteditor_videobtn')){let url=e.target.getAttribute('data-videourl');if(url){let iframe=document.createElement('iframe');iframe.src=url;new M.recit.reciteditor.Popup(iframe)}
e.preventDefault()}else if(e.target&&e.target.classList.contains('attoreciteditor_img-popup')){let url=e.target.src;if(url){let img=document.createElement('img');img.src=url;new M.recit.reciteditor.Popup(img)}
e.preventDefault()}else if(e.target&&e.target.matches('.attoreciteditor_flipcard2 *')){let el=e.target;while(el=el.parentElement){if(el.classList.contains('attoreciteditor_flipcard2')){break}}
if(!el)return;if(el.classList.contains("hover2")){el.classList.remove('hover2')}else{el.classList.add('hover2')}
e.preventDefault()}})
import requests
import os
import time
import pickle
import copy
import logging
import matplotlib.pyplot as plt


class _LoginHandler:
    def __init__(self):
        self.__index_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36 ',
            'upgrade-insecure-requests': '1',
            'set-fetch-user': '?1',
            'set-fetch-site': 'none',
            'set-fetch-mode': 'navigate'
        }
        self.__index_url = 'https://www.zhihu.com'
        self.__captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        self.__udid_url = 'https://www.zhihu.com/udid'
        self.__get_token_url = 'https://www.zhihu.com/api/v3/account/api/login/qrcode'
        self.__qrcode_file_url = os.path.expanduser('~') + '\\zhqrcode.png'
        self.__cookies_file_path = os.path.expanduser('~') + '\\.zh'
        self.__session = requests.session()
        self.__logger = None

    def login(self, remember_me: bool = True, logger: logging.Logger = None) -> requests.Session:
        """
        Login Zhihu by scanning the QRCode, or loading the local cookies.
        If remember_me is True, the cookies will be saved in your disk so that you can login without QRCode next time.

        :param remember_me: save the cookies if True. Default True.
        :param logger: give a logger to output log. Default None.
        :return: requests.Session
        """
        self.__logger = logger
        try:
            self.__load_cookie()
            if self.__logger is not None:
                self.__logger.info('load cookies to login successfully!')
        except FileNotFoundError:
            self.__qrcode_login(remember_me)
            if self.__logger is not None:
                self.__logger.info('scan QRCode to login successfully!')

        return copy.deepcopy(self.__session)

    def get_session(self) -> requests.Session:
        """
        Use this after login() to get the session. If you use this before login(), you will get an empty session.

        :return: requests.Session.
        """
        return copy.deepcopy(self.__session)

    def get_visit_headers(self) -> dict:
        """
        get the headers which can visit Zhihu successfully.

        :return: https headers.
        """
        return copy.deepcopy(self.__index_headers)

    def __load_cookie(self):
        cookie_file = open(self.__cookies_file_path, 'rb')
        self.__session.cookies.update(pickle.load(cookie_file))
        cookie_file.close()

    def __qrcode_login(self, remember_me):
        if self.__logger is not None:
            self.__logger.debug('preparing necessary cookies to login...')

        self.__session.get(self.__index_url, headers=self.__index_headers)
        index_cookies_dict = requests.utils.dict_from_cookiejar(self.__session.cookies)
        login_headers = self.__get_login_headers(index_cookies_dict)

        self.__session.get(self.__captcha_url, headers=login_headers)
        self.__session.post(self.__udid_url, headers=login_headers)

        token_res = self.__session.post(self.__get_token_url, headers=login_headers).json()
        if self.__logger is not None:
            self.__logger.debug('downloading QRCode...')
        qrcode_res = self.__session.get(self.__get_token_url + '/%s/image' % token_res['token'],
                                        headers=login_headers)
        with open(self.__qrcode_file_url, 'wb') as f:
            f.write(qrcode_res.content)
        self.__open_qrcode()
        if self.__logger is not None:
            self.__logger.debug('show QRCode')

        while True:
            if self.__logger is not None:
                self.__logger.debug('wait for user scanning...')

            self.__session.get(self.__get_token_url + '/%s/scan_info' % token_res['token'], headers=login_headers)
            cur_cookies_dict = requests.utils.dict_from_cookiejar(self.__session.cookies)
            if 'z_c0' in cur_cookies_dict.keys():
                plt.close()
                if remember_me:
                    if self.__logger is not None:
                        self.__logger.debug('save cookies')
                    self.__save_cookie()
                break

            time.sleep(2)

    def __get_login_headers(self, cur_cookies_dict):
        return {
            'x-ab-param': 'se_use_zitem=0;tp_sft=a;soc_zcfw_badcase=0;top_quality=0;li_qa_btn_text=0;li_de=no'
                          ';se_famous=1;ug_follow_topic_1=2;li_tjys_ec_ab=0;li_vip_lr=0;se_billboardsearch=0'
                          ';se_rel_search=0;tp_club_qa=1;ug_follow_answerer=0;li_qa_new_cover=1;se_websearch=3'
                          ';se_multi_task_new=2;tp_club_pk=1;pf_newguide_vertical=0;ls_fmp4=0;zr_answer_rec_cp=open'
                          ';zr_search_satisfied=0;ug_goodcomment_0=1;li_purchase_test=0;tsp_redirecthotlist=1'
                          ';tp_topic_rec=1;zr_video_rec_fs=default;se_lottery=0;soc_brdcst4=0;tsp_feiyanfangzhi=1'
                          ';li_se_section=0;qap_question_visitor= '
                          '0;se_likebutton=0;soc_notification=0;top_ebook=0;tp_header_style=1;se_college=default'
                          ';tp_club_header=1;se_site_onebox=0;se_zu_recommend=0;tp_club_tab=0;se_entity_model=0'
                          ';se_subtext=0;zr_rec_answer_cp=close;soc_authormore=2;li_se_media_icon=1'
                          ';soc_zcfw_broadcast=0;soc_newfeed=0;pf_creator_card=1;li_android_vip=0;se_new_topic=0'
                          ';se_whitelist=0;soc_bigone=0;zr_km_answer=open_cvr;se_mobileweb=1;tp_qa_toast=1'
                          ';se_webtimebox=0;ls_zvideo_license=1;se_cardrank_1=0;tp_qa_metacard=1;se_p_slideshow=0'
                          ';se_cardrank_4=1;tp_score_1=a;soc_brdcst3=0;top_v_album=1;top_universalebook=1'
                          ';zr_km_sku_mix=sku_20;zr_se_new_xgb=0;zr_article_new=close;tp_club_android_join=0'
                          ';zw_sameq_sorce=999;ug_follow_answerer_0=0;qap_payc_invite=0;se_multianswer=0;zr_km_style'
                          '=base;se_cp2=0;li_video_section=0;zr_video_recall=current_recall;tp_m_intro_re_topic=1'
                          ';ug_zero_follow_0=0;li_se_heat=1;zr_km_sku_thres=false;zr_expslotpaid=1;se_ltr_cp_new=0'
                          ';se_payconsult=0;se_adxtest=1;tp_meta_card=0;tp_qa_metacard_top=top;li_salt_hot=0;tsp_vote'
                          '=2;ug_newtag=0;soc_zuichangfangwen=0;se_pek_test=1;se_sug=1;se_topiclabel=1;soc_bignew=1'
                          ';top_test_4_liguangyi=1;se_webmajorob=0;top_hotcommerce=1;se_wannasearch=0;se_agency= '
                          '0;zr_paid_answer_exp=0;se_topicfeed=0;se_cardrank_2=1;se_hotsearch=0;top_ydyq=X'
                          ';qap_ques_invite=0;zw_payc_qaedit=0;se_hotmore=2;se_featured=1;tp_topic_head=0'
                          ';ug_fw_answ_aut_1=0;li_sc=no;se_club_post=5;se_hot_timebox=0;se_cardrank_3=0;se_cbert=0'
                          ';tp_club_join=0;zr_slot_cold_start=aver;se_sug_entrance=0;se_bert_v2=0;se_zu_onebox=0'
                          ';se_preset_tech=0;se_amovietab=1;li_query_match=0;qap_thanks=1;li_se_across=0;top_root=0'
                          ';se_ctx_rerank=0;se_waterfall=0;tp_topic_entry=0;se_related_index=3;se_backsearch=0'
                          ';se_member_rescore=0;soc_zcfw_broadcast2=1;pf_noti_entry_num=0;se_spb309=0;se_colorfultab'
                          '=1;se_pek_test3=1;se_ad_index=10;soc_wonderuser_recom=2;zr_video_rank_nn=new_rank'
                          ';se_entity_model_14=0;tp_topic_tab=0;pf_fuceng=1;li_cln_vl=no;li_answer_card=0'
                          ';se_dnn_unbias=1;se_college_cm=0;ls_videoad=2;li_qc_pt=0;zr_rel_search=base;soc_special=0'
                          ';soc_yxzl_zcfw=0;top_new_feed=5;li_svip_tab_search=0;zr_art_rec=base;se_ltr_dnn_cp=0'
                          ';tp_club_qa_pic=1;soc_stickypush=0;li_vip_no_ad_mon=0;se_webrs=1;tp_club_feed=1'
                          ';se_col_boost=0;soc_ri_merge=0;ls_zvideo_rec=2;li_album_liutongab=0;se_ios_spb309=0'
                          ';se_preset_label=1;se_movietab=1;tp_topic_style=0;zr_km_slot_style=event_card'
                          ';zr_slot_training=1;qap_question_author=0;se_expired_ob=0;zr_des_detail=0;soc_update=1'
                          ';soc_leave_recommend=2;li_pay_banner_type=6;li_sku_bottom_bar_re=0;zr_ans_rec=gbrank'
                          ';zr_km_feed_nlp=old;zr_slotpaidexp=1;se_senet=0;tp_sft_v2=d;li_answer_right=0'
                          ';soc_zcfw_shipinshiti=0;se_suggest_cache=0;tp_sticky_android=2;ug_zero_follow=0'
                          ';se_auto_syn=0;se_time_threshold=0;tsp_hotlist_ui=1;se_timebox_up=0;se_search_feed=N'
                          ';li_paid_answer_exp=0;li_hot_score_ab=0;li_answer_label=0;sem_up_growth=in_app'
                          ';li_ebook_audio=0;se_pek_test2=1;zr_test_aa1=0;se_new_merger=1;pf_foltopic_usernum=50'
                          ';li_qa_cover=old;zr_intervene=0;soc_cardheight=0;zr_video_rank=new_rank;se_aa_base=0'
                          ';ls_recommend_test=0 ',
            'x-requested-with': 'fetch',
            'x-xsrftoken': cur_cookies_dict['_xsrf'],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71 ',
            'set-fetch-mode': 'cors',
            'set-fetch-site': 'same-origin',
            'origin': 'https://www.zhihu.com',
            'referer': 'https://www.zhihu.com/signin?next=%2F'
        }

    def __save_cookie(self):
        cookie_file = open(self.__cookies_file_path, 'wb')
        pickle.dump(self.__session.cookies, cookie_file)
        cookie_file.close()

    def __open_qrcode(self):
        p = plt.imread(self.__qrcode_file_url)
        plt.ion()
        plt.axis('off')
        plt.imshow(p)
        plt.pause(0.5)


login_handler = _LoginHandler()

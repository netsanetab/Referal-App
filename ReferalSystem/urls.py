
from django.contrib import admin
from django.urls import path
from Referal import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home_view,name=''),

    path('adminclick', views.adminclick_view),
    # path('customerclick', views.customerclick_view),
    path('regionadminclick', views.regionaladminclick_view),

    # path('customersignup', views.customer_signup_view,name='customersignup'),
    # path('mechanicsignup', views.mechanic_signup_view,name='mechanicsignup'),
                                                                            
    path('customerlogin', LoginView.as_view(template_name='Referal/customerlogin.html'),name='customerlogin'),
    path('regionaladminlogin', LoginView.as_view(template_name='Referal/regionaladminlogin.html'),name='regionaladminlogin'),
    path('ceologin', LoginView.as_view(template_name='Referal/ceologin.html'),name='ceologin'),
    path('adminlogin', LoginView.as_view(template_name='Referal/adminlogin.html'),name='adminlogin'),



    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    # path('admin-liaizon', views.admin_customer_view,name='admin-liaizon'),
    # path('admin-view-customer',views.admin_view_customer_view,name='admin-view-customer'),
    # path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    # path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    
    path('admin-add-liaizon', views.admin_add_Liaizon_view,name='admin-add-liaizon'),
    path('regionaladmin-add-Liaizonusers',views.regionaladmin_add_Liaizonusers_view,name='regionaladmin-add-Liaizonusers'),
    path('regionaladmin-add-Liaizonusers-save',views.regionaladmin_add_Liaizonusers_view_save,name='regionaladmin-add-Liaizonusers-save'),
    
    path('regional_admin_view_users',views.regional_admin_view_users,name='regional_admin_view_users'),

    path('regionaladmin-add-ceousers',views.regionaladmin_add_ceo_view,name='regionaladmin-add-ceousers'),
    path('regionaladmin-add-ceousers-save',views.regionaladmin_add_ceo_view_save,name='regionaladmin-add-ceousers-save'),
    
    # path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view,name='admin-view-customer-enquiry'),
    # path('admin-view-customer-invoice', views.admin_view_customer_invoice_view,name='admin-view-customer-invoice'),


    # path('admin-request', views.admin_request_view,name='admin-request'),
    # path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    # path('change-status/<int:pk>', views.change_status_view,name='change-status'),
    # path('admin-delete-request/<int:pk>', views.admin_delete_request_view,name='admin-delete-request'),
    # path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    # path('admin-approve-request',views.admin_approve_request_view,name='admin-approve-request'),
    # path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),

    path('liaizon_approve_request/',views.liaizon_approve_request_view,name='liaizon_approve_request'),
    path('liaizon_view_all_request/',views.liaizon_view_all_request,name='liaizon_view_all_request'),
    path('ceo_view_all_request/',views.ceo_view_all_request,name='ceo_view_all_request'),
    path('liaizon_view_all_feedback/',views.liaizon_view_all_feedback,name='liaizon_view_all_feedback'),
    path('ceo_view_all_feedback/',views.ceo_view_all_feedback,name='ceo_view_all_feedback'),
    path('patient-detail/<int:pk>',views.patient_detail_view,name='patient-detail'),
    path('patient_print_detail/<int:pk>',views.patient_print_detail,name='patient_print_detail'),
    path('patient_print_all/',views.patient_print_all,name='patient_print_all'),

    path('patient_detail2_view/<int:pk>',views.patient_detail2_view,name='patient_detail2_view'),
    path('ceo_print_all/',views.ceo_print_all,name='ceo_print_all'),

    path('update_approve_status/<int:pk>',views.update_approve_status,name='update_approve_status'),
    path('liaizon_feedback_referal/',views.liaizon_feedback_referal_view,name='liaizon_feedback_referal'),
    path('Liaizon-request/<int:pk>',views.Liaizon_request_view,name='Liaizon-request'),
    path('re_refer_request/<int:pk>',views.re_refer_request,name='re_refer_request'),
    path('re_referal_request_save_view',views.re_referal_request_save_view,name='re_referal_request_save_view'),

    path('manage_ward/',views.manage_ward, name='manage_ward'),
    path('add_ward',views.add_ward, name='add_ward'),
    path('add_ward_save',views.add_ward_save, name='add_ward_save'),
    path('edit_ward/<str:pk>',views.edit_ward, name="edit_ward"),
    path('edit_ward_save',views.edit_ward_save, name='edit_ward_save'),
    path('view_ward/<str:pk>',views.view_ward, name="view_ward"),
    path('delete_ward/<str:pk>',views.delete_ward, name="delete_ward"),

    path('add_room_save',views.add_room_save, name='add_room_save'),
    path('edit_room_save',views.edit_room_save, name='edit_room_save'),
    path('delete_room/<str:pk>',views.delete_room, name="delete_room"),
    

    path('manage_patient/',views.manage_patient, name='manage_patient'),
    path('add_patient',views.add_patient, name='add_patient'),
    path('add_patient_save',views.add_patient_save, name='add_patient_save'),
    path('edit_patient/<str:pk>',views.edit_patient, name="edit_patient"),
    path('edit_patient_save',views.edit_patient_save, name='edit_patient_save'),

    path('manage_appointment/',views.manage_appointment, name='manage_appointment'),
    path('add_appointment',views.add_appointment, name='add_appointment'),
    path('add_appointment_save',views.add_appointment_save, name='add_appointment_save'),
    path('edit_appointment/<str:pk>',views.edit_appointment, name="edit_appointment"),
    path('edit_appointment_save',views.edit_appointment_save, name='edit_appointment_save'),
    path('delete_appointment/<str:pk>',views.delete_appointment, name="delete_appointment"),

    path('manage_service/',views.manage_service, name='manage_service'),
    path('add_service',views.add_service, name='add_service'),
    path('add_service_save',views.add_service_save, name='add_service_save'),
    path('edit_service/<str:pk>',views.edit_service, name="edit_service"),
    path('edit_service_save',views.edit_service_save, name='edit_service_save'),
    path('delete_service/<str:pk>',views.delete_service, name="delete_service"),

    # path('admin-view-service-cost',views.admin_view_service_cost_view,name='admin-view-service-cost'),
    # path('update-cost/<int:pk>', views.update_cost_view,name='update-cost'),

    # path('admin-regionaladmin', views.admin_mechanic_view,name='admin-regionaladmin'),
    # path('admin-view-mechanic',views.admin_view_mechanic_view,name='admin-view-mechanic'),
    # path('delete-mechanic/<int:pk>', views.delete_mechanic_view,name='delete-mechanic'),
    # path('update-mechanic/<int:pk>', views.update_mechanic_view,name='update-mechanic'),
    # path('admin-add-mechanic',views.admin_add_mechanic_view,name='admin-add-mechanic'),
    # path('admin-approve-mechanic',views.admin_approve_mechanic_view,name='admin-approve-mechanic'),
    # path('approve-mechanic/<int:pk>', views.approve_mechanic_view,name='approve-mechanic'),
    # path('delete-mechanic/<int:pk>', views.delete_mechanic_view,name='delete-mechanic'),
    # path('admin-view-mechanic-salary',views.admin_view_mechanic_salary_view,name='admin-view-mechanic-salary'),
    # path('update-salary/<int:pk>', views.update_salary_view,name='update-salary'),

    # path('admin-feedback', views.admin_feedback_view,name='admin-feedback'),


    path('regionaladmin-dashboard', views.regional_admin_dashboard_view,name='regionaladmin-dashboard'),
    # path('mechanic-work-assigned', views.mechanic_work_assigned_view,name='mechanic-work-assigned'),
    # path('mechanic-update-status/<int:pk>', views.mechanic_update_status_view,name='mechanic-update-status'),
    # path('mechanic-feedback', views.mechanic_feedback_view,name='mechanic-feedback'),
    # path('mechanic-salary', views.mechanic_salary_view,name='mechanic-salary'),
    path('regionaladmin-profile', views.regionaladmin_profile_view,name='regionaladmin-profile'),
    path('edit_regionaladmin_profile_view', views.edit_regionaladmin_profile_view,name='edit_regionaladmin_profile_view'),



    path('liaizon-dashboard', views.Facility_dashboard,name='liaizon-dashboard'),
    path('ceo-dashboard', views.Ceo_dashboard_view,name='ceo-dashboard'),
    # path('liaizon-request', views.liaizon_request_view,name='liaizon-request'),
    # path('customer-add-request',views.customer_add_request_view,name='customer-add-request'),

    path('liaizon-user-profile', views.liaizon_profile_view,name='liaizon-user-profile'),
    path('edit-liaizon-profile', views.edit_liaizon_profile_view,name='edit-liaizon-profile'),
    # path('customer-feedback', views.customer_feedback_view,name='customer-feedback'),
    # path('customer-invoice', views.customer_invoice_view,name='customer-invoice'),
    # path('liaizon-view-request',views.liaizon_view_request_view,name='liaizon-view-request'),
    # path('customer-delete-request/<int:pk>', views.customer_delete_request_view,name='customer-delete-request'),
    # path('customer-view-approved-request',views.customer_view_approved_request_view,name='customer-view-approved-request'),
    # path('customer-view-approved-request-invoice',views.customer_view_approved_request_invoice_view,name='customer-view-approved-request-invoice'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='Referal/index.html'),name='logout'),

    # path('aboutus', views.aboutus_view),
    # path('contactus', views.contactus_view),
    
    path('refere-request', views.refere_request_view,name='refere-request'),
    path('refere-request-save', views.refere_request_save_view,name='refere-request-save'),
    
    path('refere-in', views.refere_in, name='refere-in'),
    path('edit_refer_request/<str:ref_req_id>',
         views.edit_refer_request, name="edit_refer_request"),

    path('manage_facility', views.manage_facility, name="manage_facility"),
    path('edit_facility/<str:facility_id>', views.edit_facility, name="edit_facility"),
    
    path('edit_facility_save', views.edit_facility_save, name="edit_facility_save"), 
    path('delete_facility/<int:pk>',views.delete_facility,name='delete_facility'),
    path('add_facility', views.add_facility, name="add_facility"),   
    path('add_facility_save', views.add_facility_save, name="add_facility_save"),
    path('edit_fac/<str:pk>', views.edit_fac, name="edit_fac"),   
    path('edit_fac_save', views.edit_fac_save, name="edit_fac_save"),
    path('manage_facilities', views.manage_facilities, name="manage_facilities"),
    path('manage_facility_user/<str:pk>', views.manage_facility_user, name="manage_facility_user"),
    path('manage_facility_user_save', views.manage_facility_user_save, name="manage_facility_user_save"),

    path('add_regional_admin_admin', views.add_regional_admin_admin, name="add_regional_admin_admin"),   
    path('add_regional_admin_admin_save', views.add_regional_admin_admin_save, name="add_regional_admin_admin_save"),
    path('view_regional_admins', views.view_regional_admins, name="view_regional_admins"),
    path('edit_regional_admin/<str:pk>', views.edit_regional_admin, name="edit_regional_admin"), 
    path('edit_regional_admin_save', views.edit_regional_admin_save, name="edit_regional_admin_save"),
    path('delete_regional_admin/<str:pk>', views.delete_regional_admin, name="delete_regional_admin"),  
      
    path('admin_report_one', views.admin_report_one, name="admin_report_one"),   
    path('regional_admin_report_one', views.regional_admin_report_one, name="regional_admin_report_one"),   

#     path('media/<path>', serve,{'document_root':       settings.MEDIA_ROOT}), 
#     path('static/<path>', serve,{'document_root': settings.STATIC_ROOT}), 


]
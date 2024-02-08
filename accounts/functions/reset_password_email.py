HTML_FORMAT = '''<html lang="en-US">

<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>Reset Password Email Template</title>
    <meta name="description" content="Reset Password Email Template.">
    <style type="text/css">
        a:hover {text-decoration: underline !important;}
    </style>
</head>

<body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
    <!--100% body table-->
    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
        style="@import url(https://fonts.cdnfonts.com/css/dm-sans); font-family: 'DM Sans', sans-serif;">
        <tr>
            <td>
                <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                    align="center" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                          <a href="https://rakeshmandal.com" title="logo" target="_blank">
                            <img width="200" src="https://i.ibb.co/SQ9mfVy/outstrip-seo.png" title="logo" alt="logo">
                          </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td>
                            <table width="95%" border="0" align="center" cellpadding="0" cellspacing="0"
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="padding:0 35px;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">
                                          Réinitialisation de votre mot de passe
                                        </h1>
                                        <span
                                            style="display:inline-block; vertical-align:middle; margin:29px 0 26px; border-bottom:1px solid #cecece; width:100px;"></span>
                                        <p style="color:#455056; font-size:15px;line-height:24px; margin:0;">
                                          Pour réinitialiser votre mot de passe, veuillez suivre les étapes ci-dessous :
                                        </p>
                                        <p>
                                        1 - Cliquez sur le lien suivant pour accéder à la page de réinitialisation du mot de passe :
                                        </p>
                         '''   
LINK_BUTTON = '''
                                        <a href="{link}"
                                            style="background:#9372F1;text-decoration:none !important; font-weight:500; margin-top:5px; margin-bottom:5px; color:#fff;text-transform:uppercase; font-size:14px;padding:10px 24px;display:inline-block;border-radius:10px;">
                                          Réinitialiser le mot de passe
                                        </a>
                                          '''
OTP_NUMBER = '''                        <p>   
                                        2 - Saisissez le code OTP suivant : <div style="font-weight:600; color:#9372F1; font-size:14px;">{otp}</div>
                                        </p>
'''
OTHER = ''' 
                                        <p> 
                                        3 - Choisissez un nouveau mot de passe fort et sécurisé.
                                        </p>
                                        <p>
                                        4 - Confirmez votre nouveau mot de passe.
                                        </p>
                                        <p>
                                        5 - Cliquez sur le bouton "Réinitialiser le mot de passe".
                                        </p>
                                        <p>
                                        Votre mot de passe sera réinitialisé avec succès !
                                        </p>
                                      
                                        
                                        
                                    </td>
                                </tr>
                                <tr>
                                    <td style="height:40px;">
                                        &nbsp;
                                    </td>
                                </tr>
                            </table>
                        </td>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:18px; margin:0 0 0;">&copy; <strong></strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    <!--/100% body table-->
</body>

</html>
'''

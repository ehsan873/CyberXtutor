from string import Template


def get_email_template(userid, passowrd, school):
    html_code = """
    \
    <head>
    <title>
    
    </title>
    <!--[if !mso]><!-- -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <!--<![endif]-->
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style type="text/css">
        #outlook a {
           
        }
    
        .ReadMsgBody {
            width: 100%;
        }
    
        .ExternalClass {
            width: 100%;
        }
    
        .ExternalClass * {
            line-height: 100%;
        }
    
        body {
            margin: 0;
            
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }
    
        table,
        td {
            border-collapse: collapse;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }
    
        img {
            border: 0;
            height: auto;
            line-height: 100%;
            outline: none;
            text-decoration: none;
            -ms-interpolation-mode: bicubic;
        }
    
        p {
            display: block;
            margin: 13px 0;
        }
    </style>
    <!--[if !mso]><!-->
    <style type="text/css">
        @media only screen and (max-width:480px) {
            @-ms-viewport {
                width: 320px;
            }
            @viewport {
                width: 320px;
            }
        }
    </style>
    <!--<![endif]-->
    <!--[if mso]>
        <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
    <!--[if lte mso 11]>
        <style type="text/css">
          .outlook-group-fix { width:100% !important; }
        </style>
        <![endif]-->
    
    
    <style type="text/css">
        @media only screen and (min-width:480px) {
            .mj-column-per-100 {
                width: 100% !important;
            }
        }
    </style>
    
    
    <style type="text/css">
    </style>
    
    </head>
    
    <body style="background-color:#f9f9f9;">
    
    
    <div style="background-color:#f9f9f9;">
    
    
        <!--[if mso | IE]>
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    
    
        <div style="background:#f9f9f9;background-color:#f9f9f9;Margin:0px auto;max-width:600px;">
    
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#f9f9f9;background-color:#f9f9f9;width:100%;">
                <tbody>
                    <tr>
                        <td style="border-bottom:#333957 solid 5px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                            <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
        </tr>
      
                  </table>
                <![endif]-->
                        </td>
                    </tr>
                </tbody>
            </table>
    
        </div>
    
    
        <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    
    
        <div style="background:#fff;background-color:#fff;Margin:0px auto;max-width:600px;">
    
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%;">
                <tbody>
                    <tr>
                        <td style="border:#dddddd solid 1px;border-top:0px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                            <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               style="vertical-align:bottom;width:600px;"
            >
          <![endif]-->
    
                            <div classes="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;">
    
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:bottom;" width="100%">
    
                                    <tr>
                                        <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
    
                                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                                <tbody>
                                                    <tr>
                                                        <td style="width:180px;">
    
                                                             <img src="https://www.reportify.in/images/abstracts/logo-line.png" alt="Reportify" width="180" height="auto">
    
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
    
                                        </td>
                                    </tr>
    
                                    <tr> <td align="center" style="font-size:0px;padding:10px 
                                    25px;padding-bottom:40px;word-break:break-word;">
    
                                            <div style="font-family:'Helvetica Neue',Arial,
                                            sans-serif;font-size:28px;font-weight:bold;line-height:1;text-align
                                            :center;color:#555;"> Welcome to Reportify </div>
    
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
    
                                            <div style="font-family:'Helvetica Neue',Arial, 
                                            sans-serif;font-size:16px;line-height:22px;text-align:left;color:#555;"> 
                                            Hello $school <br></br>
                                             <br></br>
                                             We are delighted to welcome you to <b>Reportify</b> and 
                                            thank you for choosing our platform. Your registration is now complete, 
                                            and we are thrilled to have you as part of our community! <br><br>
                                            your account information is as follows:<br>
                                            </div>
    
                                        </td>
                                    </tr>
                                     <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
    
                                            <div style="font-family:'Helvetica Neue',Arial,
                                            sans-serif;font-size:16px;line-height:22px;text-align:left;color:#555;"> 
                                            Username: $userid <br></br> Password: $password </div>
    
                                        </td>
                                    </tr>
                                     <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
    
                                            <div style="font-family:'Helvetica Neue',Arial, 
                                            sans-serif;font-size:16px;line-height:22px;text-align:left;color:#555;"> 
                                            Please keep your login credentials safe and secure. We recommend that you 
                                            change your password immediately upon logging in for the first 
                                            time.<br><br> We take the security of our platform seriously and are 
                                            committed to providing you with the best user experience. If you have any 
                                            questions or concerns, please do not hesitate to contact us at 
                                            support@reportify.in. Our team is always ready to assist you.<br><br> 
                                            Once again, welcome to Reportify, and thank you for choosing us.

                                            
                                            </div>
    
                                        </td>
                                    </tr>
    
                                    <tr> <td align="center" style="font-size:0px;padding:10px 
                                    25px;padding-top:30px;padding-bottom:50px;word-break:break-word;">
    
                                            <table align="center" border="0" cellpadding="0" cellspacing="0" 
                                            role="presentation" style="border-collapse:separate;line-height:100%;"> 
                                            <tr> <td align="center" bgcolor="#00A1B1" role="presentation" 
                                            style="border:none;border-radius:3px;color:#ffffff;cursor:auto;padding 
                                            :15px 25px;" valign="middle"> <p style="Margin: 0;"> <a 
                                            href="https://reportify.in" 
                                            style="background:#00A1B1;color:#ffffff;font-family:'Helvetica Neue',
                                            Arial,
                                            sans-serif;font-size:15px;font-weight:normal;line-height:120%;Margin:0
                                            ;text-decoration:none;text-transform:none;display:inline-block;padding
                                            :10px 10px;border-radius:10px">Login to Your Account</a> </p> </td> </tr> </table>
    
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
    
                                            <div style="font-family:'Helvetica Neue',Arial,
                                            sans-serif;font-size:14px;line-height:20px;text-align:left;color:#525252
                                            ;"> Best regards,<br>
                                             Reportify<br> 
                                             <a href="reportify.in">Reportify</a>
                                              </div>
    
                                        </td>
                                    </tr>
    
                                </table>
    
                            </div>
    
                            <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                        </td>
                    </tr>
                </tbody>
            </table>
    
        </div>
    
    
        <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    
    
        <div style="Margin:0px auto;max-width:600px;">
    
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                            <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               style="vertical-align:bottom;width:600px;"
            >
          <![endif]-->
    
                            <div classes="mj-column-per-100 outlook-group-fix" 
                            style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align
                            :bottom;width:100%;">
    
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                    <tbody>
                                        <tr>
                                            <td style="vertical-align:bottom;padding:0;">
    
                                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
    
                                                    <tr>
                                                        <td align="center" style="font-size:0px;padding:0;word-break:break-word;">
    
                                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:12px;font-weight:300;line-height:1;text-align:center;color:#575757;">
                                                                DLF Cyber City, DLF Phase 3, Gurgaon
                                                            </div>
    
                                                        </td>
                                                    </tr>
    
                                                    <tr>
                                                        <td align="center" style="font-size:0px;padding:10px;word-break:break-word;">
    
                                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:12px;font-weight:300;line-height:1;text-align:center;color:#575757;">
                                                                <a href="" style="color:#575757">Unsubscribe</a> from our emails
                                                            </div>
    
                                                        </td>
                                                    </tr>
    
                                                </table>
    
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
    
                            </div>
    
                            <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                        </td>
                    </tr>
                </tbody>
            </table>
    
        </div>
    
    
        <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      <![endif]-->
    
    
    </div>
    
    </body>
    
    </html>
    """

    values = {
        'userid': userid,
        'password': passowrd,
        'school': school,
    }
    template = Template(html_code)
    formatted_html = template.substitute(values)

    return formatted_html


def get_forget_password_email_temmplete():
    html_code = """
    <!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
    <title>

    </title>
    <!--[if !mso]><!-- -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <!--<![endif]-->
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style type="text/css">
        #outlook a {
            padding: 0;
        }

        .ReadMsgBody {
            width: 100%;
        }

        .ExternalClass {
            width: 100%;
        }

        .ExternalClass * {
            line-height: 100%;
        }

        body {
            margin: 0;
            padding: 0;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }

        table,
        td {
            border-collapse: collapse;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }

        img {
            border: 0;
            height: auto;
            line-height: 100%;
            outline: none;
            text-decoration: none;
            -ms-interpolation-mode: bicubic;
        }

        p {
            display: block;
            margin: 13px 0;
        }
    </style>
    <!--[if !mso]><!-->
    <style type="text/css">
        @media only screen and (max-width:480px) {
            @-ms-viewport {
                width: 320px;
            }
            @viewport {
                width: 320px;
            }
        }
    </style>
    <!--<![endif]-->
    <!--[if mso]>
        <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
    <!--[if lte mso 11]>
        <style type="text/css">
          .outlook-group-fix { width:100% !important; }
        </style>
        <![endif]-->


    <style type="text/css">
        @media only screen and (min-width:480px) {
            .mj-column-per-100 {
                width: 100% !important;
            }
        }
    </style>


    <style type="text/css">
    </style>

</head>

<body style="background-color:#f9f9f9;">


    <div style="background-color:#f9f9f9;">


        <!--[if mso | IE]>
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->


        <div style="background:#f9f9f9;background-color:#f9f9f9;Margin:0px auto;max-width:600px;">

            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#f9f9f9;background-color:#f9f9f9;width:100%;">
                <tbody>
                    <tr>
                        <td style="border-bottom:#333957 solid 5px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                            <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
        </tr>
      
                  </table>
                <![endif]-->
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>


        <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->


        <div style="background:#fff;background-color:#fff;Margin:0px auto;max-width:600px;">

            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%;">
                <tbody>
                    <tr>
                        <td style="border:#dddddd solid 1px;border-top:0px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                            <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               style="vertical-align:bottom;width:600px;"
            >
          <![endif]-->

                            <div classes="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;">

                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:bottom;" width="100%">

                                    <tr>
                                        <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                                <tbody>
                                                    <tr>
                                                        <td style="width:64px;">

                                                            <img height="auto" src="https://www.reportify.in/images/abstracts/logo-line.png" style="border:0;display:block;outline:none;text-decoration:none;width:100%;" width="64" />

                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>

                                        </td>
                                    </tr>

                                    <tr>
                                        <td align="center" style="font-size:0px;padding:10px 25px;padding-bottom:40px;word-break:break-word;">

                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:22px;font-weight:bold;line-height:1;text-align:center;color:#555;">
                                                Uh-oh! Your Reportify free trial just ended!
                                            </div>

                                        </td>
                                    </tr>

                                    <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                            <div style="font-family:'Helvetica Neue',Arial,
                                            sans-serif;font-size:16px;line-height:22px;text-align:left;color:#555;"> 
                                            Your free trial of Reportify has ended, we're excited to get you 
                                            started with your Reportify account. To give you some time to enter in 
                                            your payment info we'll still collect all your data for the next 30 days. 
                                            </div>

                                        </td>
                                    </tr>

                                    <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:16px;line-height:22px;text-align:left;color:#555;">
                                                In the meanwhile, you'll no longer have access to these benefits:
                                            </div>

                                        </td>
                                    </tr>

                                    <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:16px;line-height:22px;text-align:left;color:#555;">
                                                - Our awesome benefit #1<br> - Our awesome benefit #2<br> - Our awesome benefit #3<br>
                                            </div>

                                        </td>
                                    </tr>

                                    <tr>
                                        <td align="center" style="font-size:0px;padding:10px 25px;padding-top:30px;word-break:break-word;">

                                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
                                                <tr>
                                                    <td align="center" bgcolor="#2F67F6" role="presentation" style="border:none;border-radius:3px;color:#ffffff;cursor:auto;padding:15px 25px;" valign="middle">
                                                        <p style="background:#2F67F6;color:#ffffff;font-family:'Helvetica Neue',Arial,sans-serif;font-size:15px;font-weight:normal;line-height:120%;Margin:0;text-decoration:none;text-transform:none;">
                                                            Update Your Billing Info
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>

                                        </td>
                                    </tr>

                                    <tr>
                                        <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:16px;line-height:22px;text-align:center;color:#555;">
                                                Or..
                                            </div>

                                        </td>
                                    </tr>

                                    <tr>
                                        <td align="center" style="font-size:0px;padding:10px 25px;padding-bottom:50px;word-break:break-word;">

                                            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
                                                <tr>
                                                    <td align="center" bgcolor="#2F67F6" role="presentation" style="border:none;border-radius:3px;color:#ffffff;cursor:auto;padding:15px 35px;" valign="middle">
                                                        <p style="background:#2F67F6;color:#ffffff;font-family:'Helvetica Neue',Arial,sans-serif;font-size:15px;font-weight:normal;line-height:120%;Margin:0;text-decoration:none;text-transform:none;">
                                                            Get A Trial Extension
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>

                                        </td>
                                    </tr>

                                    <tr>
                                        <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">

                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:14px;line-height:20px;text-align:left;color:#525252;">
                                                Best regards,<br><br> Csaba Kissi<br>Elerion ltd., CEO and Founder<br>
                                                <a href="https://www.htmlemailtemplates.net" style="color:#2F67F6">htmlemailtemplates.net</a>
                                            </div>

                                        </td>
                                    </tr>

                                </table>

                            </div>

                            <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>


        <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->


        <div style="Margin:0px auto;max-width:600px;">

            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                            <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               style="vertical-align:bottom;width:600px;"
            >
          <![endif]-->

                            <div classes="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;">

                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                    <tbody>
                                        <tr>
                                            <td style="vertical-align:bottom;padding:0;">

                                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">

                                                    <tr>
                                                        <td align="center" style="font-size:0px;padding:0;word-break:break-word;">

                                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:12px;font-weight:300;line-height:1;text-align:center;color:#575757;">
                                                                Some Firm Ltd, 35 Avenue. City 10115, USA
                                                            </div>

                                                        </td>
                                                    </tr>

                                                    <tr>
                                                        <td align="center" style="font-size:0px;padding:10px;word-break:break-word;">

                                                            <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:12px;font-weight:300;line-height:1;text-align:center;color:#575757;">
                                                                <a href="" style="color:#575757">Unsubscribe</a> from our emails
                                                            </div>

                                                        </td>
                                                    </tr>

                                                </table>

                                            </td>
                                        </tr>
                                    </tbody>
                                </table>

                            </div>

                            <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>


        <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      <![endif]-->


    </div>

</body>

</html>
    
    """
    values = {
        'userid': "Asad",
        'password': 'asdasd ',
        'school': "IIM Lucknow campus Noida",
    }
    template = Template(html_code)
    formatted_html = template.substitute(values)

    return formatted_html


def get_otp_email(otp):
    html_code = """
    
    
    
    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
  <div style="margin:50px auto;width:70%;padding:20px 0">
    <div style="border-bottom:1px solid #eee">
      <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Reportify</a>
    </div>
    <p style="font-size:1.1em">Hi,</p>
    <p>Use the following OTP to complete your ResetPassword procedures. OTP is valid for 5 minutes</p>
    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">$otp</h2>
    <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
    <hr style="border:none;border-top:1px solid #eee" />
    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
      <p>Reportify.in</p>
      <p>1600 Amphitheatre Parkway</p>
      <p>California</p>
    </div>
  </div>
</div>
    """
    values = {
        'otp': otp,
    }
    template = Template(html_code)
    formatted_html = template.substitute(values)

    return formatted_html

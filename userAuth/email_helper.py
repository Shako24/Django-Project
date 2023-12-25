from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache


@lru_cache()
def img_data(filepath, cid):
    with open(finders.find(filepath), 'rb') as f:
        img_data = f.read()
    img = MIMEImage(img_data)
    img.add_header('Content-ID', cid)
    return img


def emailInvoice(checkout, serviceList):
    part1 = f'''
    <!DOCTYPE html>
    <head style="box-sizing: border-box;">

    </head>
    <html style="box-sizing: border-box;">
    <body style="box-sizing: border-box;margin: 0;font-family: var(--bs-body-font-family);font-size: var(--bs-body-font-size);font-weight: var(--bs-body-font-weight);line-height: var(--bs-body-line-height);color: var(--bs-body-color);text-align: var(--bs-body-text-align);background-color: var(--bs-body-bg);-webkit-text-size-adjust: 100%;-webkit-tap-highlight-color: transparent;">
    <section class="mx-5" style="box-sizing: border-box;min-width: 0;padding: 0;margin: 0;border: 0;margin-right: 3rem!important;margin-left: 3rem!important;">
            <div class="container" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-right: auto;margin-left: auto;">
                <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                    <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">
                        <h2 class="text-danger fw-bolder" style="box-sizing: border-box;margin-top: 0;margin-bottom: .5rem;font-weight: bolder!important;line-height: 1.2;color: #c70808e6 !important;font-size: calc(1.325rem + .9vw);--bs-text-opacity: 1;">INVOICE</h2>
                        <h3 style="box-sizing: border-box;margin-top: 0;margin-bottom: .5rem;font-weight: 500;line-height: 1.2;color: var(--bs-heading-color,inherit);font-size: calc(1.3rem + .6vw);">+971 52 913 6867</h3>
                        <h4 style="box-sizing: border-box;margin-top: 0;margin-bottom: .5rem;font-weight: 500;line-height: 1.2;color: var(--bs-heading-color,inherit);font-size: calc(1.275rem + .3vw);">www.rapidcare.com</h4>
                        <h4 style="box-sizing: border-box;margin-top: 0;margin-bottom: .5rem;font-weight: 500;line-height: 1.2;color: var(--bs-heading-color,inherit);font-size: calc(1.275rem + .3vw);">Dubai,Uae</h4>
                    </div>
                    <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">
                        <img src="cid:logo" alt="logo image" style="box-sizing: border-box;vertical-align: middle;">
                    </div>
                </div>
            </div>
        </section>
        <section class="mx-5" style="box-sizing: border-box;min-width: 0;padding: 0;margin: 0;border: 0;margin-right: 3rem!important;margin-left: 3rem!important;">
            <div class="container" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-right: auto;margin-left: auto;">
                <div class="col" style="width: 85%;border-bottom: 1px dashed #555;box-sizing: border-box;flex: 1 0 0%;"></div>
                <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                    <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">
                        <div class="row mb-3" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));margin-bottom: 1rem!important;"><span style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);">INVOICE TO: {checkout.user}</span></div>
                        <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));"><span style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);">Dubai UAE</span></div>
                    </div>
                    <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">
                        <span class="fw-bold" style="box-sizing: border-box;font-weight: 700!important;">
                            REF NO.: {checkout.id}
                        </span> <br style="box-sizing: border-box;">
                        <span class="fw-bold" style="box-sizing: border-box;font-weight: 700!important;">
                            TRN Number: 100490730700003
                        </span> <br style="box-sizing: border-box;">
                        <span class="fw-bold" style="box-sizing: border-box;font-weight: 700!important;">
                            Invoice Generated on: {checkout.datetime}
                        </span> <br style="box-sizing: border-box;">
                        <span class="fw-bold" style="box-sizing: border-box;font-weight: 700!important;">
                            Due Date: 
                        </span>
                    </div>
                </div>
                <table class="table table-borderless mt-3 text-center" style="width: 85%;box-sizing: border-box;caption-side: bottom;border-collapse: collapse;--bs-table-color: var(--bs-body-color);--bs-table-bg: transparent;--bs-table-border-color: var(--bs-border-color);--bs-table-accent-bg: transparent;--bs-table-striped-color: var(--bs-body-color);--bs-table-striped-bg: rgba(0, 0, 0, 0.05);--bs-table-active-color: var(--bs-body-color);--bs-table-active-bg: rgba(0, 0, 0, 0.1);--bs-table-hover-color: var(--bs-body-color);--bs-table-hover-bg: rgba(0, 0, 0, 0.075);margin-bottom: 1rem;color: var(--bs-table-color);vertical-align: top;border-color: var(--bs-table-border-color);margin-top: 1rem!important;text-align: center!important;">
                    <thead class="table-dark" style="box-sizing: border-box;border-color: var(--bs-table-border-color);border-style: solid;border-width: 0;--bs-table-color: #fff;--bs-table-bg: #212529;--bs-table-border-color: #373b3e;--bs-table-striped-bg: #2c3034;--bs-table-striped-color: #fff;--bs-table-active-bg: #373b3e;--bs-table-active-color: #fff;--bs-table-hover-bg: #323539;--bs-table-hover-color: #fff;color: var(--bs-table-color);vertical-align: bottom;">
                        <tr style="box-sizing: border-box;border-color: inherit;border-style: solid;border-width: 0;">
                            <th scope="col" style="box-sizing: border-box;text-align: -webkit-match-parent;border-color: inherit;border-style: solid;border-width: 0;padding: .5rem .5rem;background-color: var(--bs-table-bg);border-bottom-width: 0;box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);">Name</th>
                            <th scope="col" style="box-sizing: border-box;text-align: -webkit-match-parent;border-color: inherit;border-style: solid;border-width: 0;padding: .5rem .5rem;background-color: var(--bs-table-bg);border-bottom-width: 0;box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);">Type</th>
                            <th scope="col" style="box-sizing: border-box;text-align: -webkit-match-parent;border-color: inherit;border-style: solid;border-width: 0;padding: .5rem .5rem;background-color: var(--bs-table-bg);border-bottom-width: 0;box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);">Description</th>
                            <th scope="col" style="box-sizing: border-box;text-align: -webkit-match-parent;border-color: inherit;border-style: solid;border-width: 0;padding: .5rem .5rem;background-color: var(--bs-table-bg);border-bottom-width: 0;box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);">Price</th>
                        </tr>
                    </thead>
                    <tbody style="box-sizing: border-box;border-color: inherit;border-style: solid;border-width: 0;vertical-align: inherit;border-top-width: 0;">
    '''
    part2 = f''''''
    for service in serviceList:

        serviceDescription = service.description.split('\n')
        part2 += f'''
                            <tr style="box-sizing: border-box;border-color: inherit;border-style: solid;border-width: 0;">
                                <th style="box-sizing: border-box;text-align: -webkit-match-parent;border-color: inherit;border-style: solid;border-width: 0;padding: .5rem .5rem;background-color: var(--bs-table-bg);border-bottom-width: 0;box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);">{service.serviceType}</th>
                                <td style="box-sizing: border-box;border-color: inherit;border-style: solid;border-width: 0;padding: .5rem .5rem;background-color: var(--bs-table-bg);border-bottom-width: 0;box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);">{service.package}</td>
                                <td style="box-sizing: border-box;border-color: inherit;border-style: solid;border-width: 0;padding: .5rem .5rem;background-color: var(--bs-table-bg);border-bottom-width: 0;box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);">'''
        
        for description in serviceDescription:
            part2 += f'''{description} <br/>'''
                                
        part2 += f'''</td>
                                <td style="box-sizing: border-box;border-color: inherit;border-style: solid;border-width: 0;padding: .5rem .5rem;background-color: var(--bs-table-bg);border-bottom-width: 0;box-shadow: inset 0 0 0 9999px var(--bs-table-accent-bg);">{service.price:.2f}</td>
                            </tr>
                '''
    part3 = f'''
                    </tbody>
                </table>
                <div class="col mx-5 pb-3" style="box-sizing: border-box;flex: 1 0 0%;margin-right: 3rem!important;margin-left: 3rem!important;padding-bottom: 1rem!important;">
                    <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                        <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;"></div>
                        <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">
                            <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">Services Total</div>
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">{checkout.servicesPrice:.2f} AED</div>
                            </div>
                            <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">Additional Costs</div>
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">{checkout.extraCost:.2f} AED</div>
                            </div>
                            <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">Discount</div>
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">{checkout.discount:.2f} AED</div>
                            </div>
                            <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">VAT</div>
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">{checkout.vat:.2f} AED</div>
                            </div>
                            <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">Total</div>
                                <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">{checkout.total:.2f} AED</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col" style="width: 85%;border-bottom: 2px dashed #555;box-sizing: border-box;flex: 1 0 0%;"></div>
                <div class="col" style="box-sizing: border-box;flex: 1 0 0%;">
                    <div class="row" style="box-sizing: border-box;--bs-gutter-x: 1.5rem;--bs-gutter-y: 0;display: flex;flex-wrap: wrap;margin-top: calc(-1 * var(--bs-gutter-y));margin-right: calc(-.5 * var(--bs-gutter-x));margin-left: calc(-.5 * var(--bs-gutter-x));">
                        <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">
                            <h2 style="box-sizing: border-box;margin-top: 0;margin-bottom: .5rem;font-weight: 500;line-height: 1.2;color: var(--bs-heading-color,inherit);font-size: calc(1.325rem + .9vw);">Terms and Condition:</h2>
                            <ul style="box-sizing: border-box;padding-left: 2rem;margin-top: 0;margin-bottom: 1rem;">
                                <li style="box-sizing: border-box;">Payment should be made in advance for any service choosen</li>
                            </ul>
                            <img src="cid:sign" alt="sign image" style="box-sizing: border-box;vertical-align: middle;">
                        </div>
                        <div class="col" style="box-sizing: border-box;flex-shrink: 0;width: 100%;max-width: 100%;padding-right: calc(var(--bs-gutter-x) * .5);padding-left: calc(var(--bs-gutter-x) * .5);margin-top: var(--bs-gutter-y);flex: 1 0 0%;">
                            <h2 style="box-sizing: border-box;margin-top: 0;margin-bottom: .5rem;font-weight: 500;line-height: 1.2;color: var(--bs-heading-color,inherit);font-size: calc(1.325rem + .9vw);">Please make payment to :</h2>
                            <p style="box-sizing: border-box;margin-top: 0;margin-bottom: 1rem;">Name: RAPID CARE CAR WASHING <br style="box-sizing: border-box;">
                                BANK: HABIB BANK ZURICH <br style="box-sizing: border-box;">
                                Account Number: AE550291090210500296268 <br style="box-sizing: border-box;">
                                <br style="box-sizing: border-box;">
                                OR
                                <br style="box-sizing: border-box;"><br style="box-sizing: border-box;">
                                CASH/PAY BY LINK
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col" style="box-sizing: border-box;flex: 1 0 0%;">
                    <h2 class="text-danger text-center fw-bolder" style="box-sizing: border-box;margin-top: 0;margin-bottom: .5rem;font-weight: bolder!important;line-height: 1.2;color: #c70808e6 !important;font-size: calc(1.325rem + .9vw);--bs-text-opacity: 1;text-align: center!important;">THANK YOU</h2>
                </div>
            </div>
        </section>


    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous" style="box-sizing: border-box;"></script>
    </body>
    </html>
    '''
    final = part1 + part2 + part3
    return final


def emailSignup():
    final = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Welcome To Rapid Care UAE!</h1>
    <p>As you explore our website, I hope you learn more about the qualities that make our company an exceptional provider of automotive and homecare services. <br><br>
        <strong>We offer service with a personal touch.</strong> <br><br>
        We have earned the trust and respect of our clients for one simple reason: we have amazing personnel. They are specialists within their fields. In all that they do, they uphold a strong service ethic. They take responsibility and satisfaction in the work that they perform. We combine enthusiasm, pride, and knowledge. <br><br>
        <strong>We positively impact the lives of people and the environment.</strong> <br><br>
        Rapid Care UAE has developed a reputation for making our customers' lives easier by providing high-quality and eco-friendly vehicle and home care services in the shortest time possible and at their convenience. <br><br>
        <strong>We adhere to a client-first approach.</strong> <br><br>
        We have only one goal: to ensure that the needs of our customers are met with the greatest degree of competency and quality at the lowest possible price. Our methodology ensures complete client satisfaction and happiness. Rapid Care's clients come to us with trust that we have the skills to take service delivery to the next level of performance. <br><br>
        As a welcome gift I would like to offer you a <strong style="font-size: larger;" >flat 20% off</strong> on all the services we are offering. To receive the discount, sequentially enter the discount codes shown below. We hope you like our services and aim to serve you better in the future. <br><br><br>
        
        <div style="display: flex; justify-content: center;">
            <img src="cid:signup" alt="signup image">
        </div>

        Best Regards, <br>
        Shayan Sayani <br>
        Founder/CEO  <br>
        </p>
</body>
</html>'''
    return final

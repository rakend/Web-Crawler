# Web Crawler

## Dealing with [SSL: CERTIFICATE_VERIFY_FAILED] error

Sample error example.

```console
HTTPSConnectionPool(host='www.somewebsite.com', port=443): Max retries exceeded with url: /url-path/ (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)')))
```

If encountered with an error as shown above or similar from log files. 
This relates to **SSLCertVerificationError** and can be fixed. 

Steps to resolve this issue.

- Update the CA(root) Certificate using pip command :
  ```console 
  pip install --upgrade certifi
  ```
  If issue still persists continue with the steps below.

- Open the URL causing issue on a browser (**Firefox** recommended).

- Download the chain of certificates from the URL and save as Base64 encoded .cer files.\
  **Chrome** : Each certificate needs to be downloaded individually.\
  **Firefox** : Entire certificate chain can be downloaded from a single file ```PEM (chain)```.\
  **Visit** : https://medium.com/@menakajain/export-download-ssl-certificate-from-server-site-url-bcfc41ea46a2.

- Find the path where **cacert.pem** is located using python.
  ```python
  import certifi
  
  path = certifi.where()
  print(path)
  ```

- Now open **cacert.pem** in notepad located from ```path``` and add every downloaded certificate contents at the end.\
  The chain of certificates should look similar to the snippet below.
  ```notepad
  -----BEGIN CERTIFICATE-----
            *****
  -----END CERTIFICATE-----
  
  -----BEGIN CERTIFICATE-----
            *****
  -----END CERTIFICATE-----
  
  -----BEGIN CERTIFICATE-----
            *****
  -----END CERTIFICATE-----
  ```

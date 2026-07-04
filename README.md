# Securing Web3Forms API Key in Portfolio

This document outlines the procedures to secure the Web3Forms `access_key` from public exposure in the frontend HTML.

---

## Method 1: Server-Side PHP Proxy (Recommended for XAMPP / Apache / PHP Hosts)

Using a backend script keeps the `access_key` completely hidden from the user's browser, preventing key harvesting and spam.

### 1. Create a `submit.php` script
Create a file named `submit.php` in the root folder of your project with the following content:

```php
<?php
// submit.php
header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input values
    $name = strip_tags(trim($_POST["name"]));
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    $message = strip_tags(trim($_POST["message"]));

    if (empty($name) || empty($message) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(["success" => false, "message" => "Please complete the form and provide a valid email."]);
        exit;
    }

    // Your private Web3Forms Access Key
    $access_key = "8fa40e2c-8ea9-4586-9088-83bf9018e54b";

    $postData = [
        'access_key' => $access_key,
        'name' => $name,
        'email' => $email,
        'message' => $message,
        'subject' => 'New Portfolio Inquiry'
    ];

    // Forward the request to Web3Forms API via curl
    $ch = curl_init('https://api.web3forms.com/submit');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($postData),
        CURLOPT_HTTPHEADER => ['Content-Type: application/json']
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    http_response_code($httpCode);
    echo $response;
} else {
    http_response_code(403);
    echo json_encode(["success" => false, "message" => "Access denied."]);
}
```

### 2. Update the frontend form in `contact.html`
Change your form element to target the local php script instead of the Web3Forms submit endpoint, and remove the hidden `access_key` input element:

```diff
- <form id="contact-form" action="https://api.web3forms.com/submit" method="POST" class="space-y-5">
-     <input type="hidden" name="access_key" value="8fa40e2c-8ea9-4586-9088-83bf9018e54b">
+ <form id="contact-form" action="submit.php" method="POST" class="space-y-5">
```

---

## Method 2: Web3Forms Domain Restriction (Alternative for Static/GitHub Pages Hosts)

If you are hosting your portfolio on a static host that does not support PHP (such as GitHub Pages or Vercel), you must keep the key in the HTML. However, you can restrict where submissions are accepted from:

1. Go to your **[Web3Forms Dashboard](https://web3forms.com/)**.
2. Locate the key: `8fa40e2c-8ea9-4586-9088-83bf9018e54b`.
3. In the key settings, look for the **Allowed Domains** / **Domain Restriction** field.
4. Input your production domain (e.g. `yourportfolio.com`).
5. Save the configuration. 

Web3Forms will now block any form submissions using this key if they do not originate from your designated web domain, securing your quota.

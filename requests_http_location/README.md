# What Is This?

A comparison of how different http clients handle redirects

Run example server

```
% python3 -m server 8080

valid_redirect_target=…
invalid_redirect_target=…
weird_redirect_target=…

Request 'http://localhost:8080/v', 'http://localhost:8080/i' or 'http://localhost:8080/w', following redirects

Press Enter when done to exit...
```

Test different clients agains either a correctly escaped redirect at `/v`, an invalid one at `/i` or a "weird" one at `/w`. (Set `USE_NIX=1` if `nix develop` is available but `go`, `cargo`, `npm`, `java` and common python http clients are not)

```
% python3 clients.py http://localhost:8080/v
```

View requested paths on the server side

```
…
Press Enter when done to exit...

<Enter>

The following paths were requested by these User-Agents:

  - /v, /v/%7E/-._~/0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C
    - Go-http-client/1.1
    - Java-http-client/21.0.5
    - Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
    - Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
    - Python-urllib/3.13
    - axios/1.8.4
    - curl/8.12.1
    - go-resty/3.0.0-beta.1 (https://resty.dev)
    - got (https://github.com/sindresorhus/got)
    - node
    - python-httpx/0.28.1
    - python-urllib3/2.3.0
    - requests-patched
    - reqwest

  - /v, /v/~/-._~/0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C
    - python-requests/2.32.3
```

# Results

As of 2025-03-28

## Valid Redirect

Redirect target:
All printable ascii characters, percent encoded except for those in the unreserved set. Also an encoded `~`, i.e. `%7E`.
```
/v/%7E/-._~/0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C
```

```
The following paths were requested by these User-Agents:

  - /v, /v/%7E/-._~/0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C
    - Go-http-client/1.1
    - Java-http-client/21.0.5
    - Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
    - Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
    - Python-urllib/3.13
    - axios/1.8.4
    - curl/8.12.1
    - go-resty/3.0.0-beta.1 (https://resty.dev)
    - got (https://github.com/sindresorhus/got)
    - node
    - python-httpx/0.28.1
    - python-urllib3/2.3.0
    - requests-patched
    - reqwest

  - /v, /v/~/-._~/0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C
    - python-requests/2.32.3
```

## Invalid Redirect

Redirect target:
All alphanumerical or punctuation ascii characters, unencoded. (except `#`, which breaks almost all clients)

```
/i/%^1%__%%/%7E/-._~/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 !"$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
```

```
The following paths were requested by these User-Agents:

  - /i, /i/%^1%__%%/%7E/-._~/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%200123456789%20!"$%&'()*+,-./:;<=>?@[\]^_`{|}~
    - Python-urllib/3.13
    - curl/8.12.1

  - /i, /i/%%5E1%__%%/%7E/-._~/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%200123456789%20!%22$%&'()*+,-./:;%3C=%3E?@[\]^_`{|}~
    - Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
    - Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0

  - /i
    - Go-http-client/1.1
    - Java-http-client/21.0.5
    - go-resty/3.0.0-beta.1 (https://resty.dev)

  - /i, /i/%^1%__%%/%7E/-._~/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%200123456789%20!%22$%&'()*+,-./:;%3C=%3E?@[\]^_`{|}~
    - axios/1.8.4
    - got (https://github.com/sindresorhus/got)
    - node
    - python-httpx/0.28.1
    - reqwest

  - /i, /i/%25%5E1%25__%25%25/%257E/-._~/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%200123456789%20!%22$%25&'()*+,-./:;%3C=%3E?@%5B%5C%5D%5E_%60%7B%7C%7D~
    - python-urllib3/2.3.0
    - requests-patched

  - /i, /i/%25%255E1%25__%25%25/~/-._~/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%25200123456789%2520!%2522$%25&'()*+,-./:;%253C=%253E?@%5B%5C%5D%5E_%60%7B%7C%7D~
    - python-requests/2.32.3
```

## Weird Redirect

Redirect target:
All printable ascii characters. All of which are percent-encoded even if they are in the unreserved set of characters

```
/w/%30%31%32%33%34%35%36%37%38%39%61%62%63%64%65%66%67%68%69%6A%6B%6C%6D%6E%6F%70%71%72%73%74%75%76%77%78%79%7A%41%42%43%44%45%46%47%48%49%4A%4B%4C%4D%4E%4F%50%51%52%53%54%55%56%57%58%59%5A%21%22%23%24%25%26%27%28%29%2A%2B%2C%2D%2E%2F%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E%5F%60%7B%7C%7D%7E%20%09%0A%0D%0B%0C
```

```
The following paths were requested by these User-Agents:

  - /w, /w/%30%31%32%33%34%35%36%37%38%39%61%62%63%64%65%66%67%68%69%6A%6B%6C%6D%6E%6F%70%71%72%73%74%75%76%77%78%79%7A%41%42%43%44%45%46%47%48%49%4A%4B%4C%4D%4E%4F%50%51%52%53%54%55%56%57%58%59%5A%21%22%23%24%25%26%27%28%29%2A%2B%2C%2D%2E%2F%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E%5F%60%7B%7C%7D%7E%20%09%0A%0D%0B%0C
    - Go-http-client/1.1
    - Java-http-client/21.0.5
    - Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
    - Python-urllib/3.13
    - axios/1.8.4
    - curl/8.12.1
    - go-resty/3.0.0-beta.1 (https://resty.dev)
    - got (https://github.com/sindresorhus/got)
    - node
    - python-httpx/0.28.1
    - python-urllib3/2.3.0
    - requests-patched
    - reqwest

  - /w, /w/%30%31%32%33%34%35%36%37%38%39%61%62%63%64%65%66%67%68%69%6A%6B%6C%6D%6E%6F%70%71%72%73%74%75%76%77%78%79%7A%41%42%43%44%45%46%47%48%49%4A%4B%4C%4D%4E%4F%50%51%52%53%54%55%56%57%58%59%5A%21%22%23%24%25%26%27%28%29%2A%2B%2C%2D.%2F%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E%5F%60%7B%7C%7D%7E%20%09%0A%0D%0B%0C
    - Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36

  - /w, /w/0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-.%2F%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C
    - python-requests/2.32.3
```

# Interpretation

In the "valid" case, only one client differs in behavior: `requests` normalizes to unescape the `%7E` to `~`.  This triggered this investigation because it broke a redirect on the public internet.

In the "weird" case, two clients touch the redirect target if it is a valid percent-encoded path:

  - `requests` normalizes to strip all escapes for unreserved characters.
  - `chrome` unescapes `.` (dot), i.e. `%2E`.

I believe this to be a rather esotheric test case because unlike `~`, which became unreserved in RFC 3986 compared to RFC 1738, alphanumeric characters were always unreserved.

For "invalid" targets, behavior differs wildly. Options seem to be:

  - Don't follow invalid redirects, raise an error: stdlib of `java`, `go`
  - Quote some invalid characters:
    - spaces only: `curl`, `urllib`
    - spaces and invalid escape sequences (still yielding invalid escape sequences): `gecko`, `chromium`
    - all characters except reserved/unreserved, ignoring invalid escape sequences: `node`, `httpx`, `got`, `reqwest`
    - all except unreserved characters (double quoting valid escape sequences): `urllib3`
    - invalid escape sequences and characters except reserved/unreserved, unquoting unreserved. Then re-escaping/double-escapint the result through `urllib3`: `requests`. Notably, this does not unquote to the same string that all other clients use (assuming the server tolerates the incorrect escape sequences)

URL shortener
# A URL shortener -  a tool that takes a long URL and turns it into short one

Below are few remarks about the task
> If a user visits the short URL, they must receive a temporary HTTP redirect to the long URL;

There are two possible HTTP request responses when using redirects, 302 and 307. 302 is used if we want the redirected pages body to appear in search engines result page, if we don’t want that – we use 307 code. This URL shortener returns 307 response code.

> Given a short URL, it must be impossible to identify the long URL, when the short URL was generated, or which user generated it, or any other metadata in any other way than via the service API;

There are few ways that a short URL can be created:
1. Getting hash value of the user input URL and trimming hash value to desired length. There are few problems with this approach. 
  * Firstly the purpose of hash algorithm is to get same value given the same input, which is not ideal since we need to get different short URL 
  given same input.
  > If the same long URL is shortened the second time, it must produce a different short URL;
  In order to get different hash value some modifications are needed to be done to the input string (for example: adding in current time as string to the input).  
  * Secondly we can't change the charakters which will be included in the hash value. For example a popular hashing algorithm -MD5 is base64 meaning that there are 64 possible values that a symbol inside 32 symbol long string can have.
  * Thirdly there is chance of collision, on rare occasions MD5 hash algorithm can return same hash value with different input.

2. Using randrange to generate random number between 0 and possible character string length.
Since we want the short URL to have 7 charakter long URL the for loop inside the algorithm would iterate 7 times generating a random number in the given interval, this random number would then index the charakter place inside a character string giving us a random short URL.
Even though we solve the problem with having a locked possible charakter string there are still some drawbacks to this approach as well.

  * There is still a possibility of this function generating a same short URL with a different inputs.

3. The solution - using random string of charakters and counters.
Upon creation of the short URL we ask the backend to give us the new short URL model instance unique id which we then pass into the function which generates a new short URL string by Floor dividing short URL id taking the remained of the operation and using that as a key in random character dictionary
  * Avoiding collision. With this approach it's almost impossible to have a collision in database since every new URL will have short URL generated from unique id
  However in a scenario where a couple instances of shorting services are running additional steps are required to handle this situation. Due to the fact that a given time couple of services may try to shorten the URL and thus creating new instances of URL models with same unique id's. This problem could be solved by assigning separate servers a range of possible counters. For example server's 1 range 0-1.000.000, server's 2 range 1.000.000-2.000.000 and so on.
  Custom character string
  Using this approach we retain possibility to customize possible characters in the short URL, for this particular implementation base58 is used. 

  Base 58 123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz
  Base 62 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

  Why base 58?
  To improve readability we use base58 since base 62 uses similar characters. The loss of possible combinations is deemed acceptable for this implementation. Since we use 7 characters in short URL string:
  Base 58 (58^7) - 2,207,984,167,552 possible combinations
  Base 62 (62^7) - 3,521,614,606,208 possible combinations
  > The characters removed are: the number zero (0), the capital letter "O", the lowercase letter "L" (l), the capital "I", the left and right quotation marks ("") and the backslash "/" symbol. 

By using any short URL creation algorithm’s discussed before there are no chance's that a user could “reverse engineer” any data from short URL.

> All the short URLs must be reasonably short and of the same length; 

For this particular implementation 7 character string has been chosen with base58 as possible characters

> It must be impossible to easily identify which of the two given short URLs was generated earlier;

It’s possible to identify which URL was created earlier, however this requires the user to create a significant amount of request concurrently. By doing this the user can figure out the base58 string by taking a closer look at the pattern in which the short URL changes.



> Provide a benchmark to showcase the speed of redirecting from short to long URLs.

Redicrent speed can be seen the  URL info page, the speed is calculated wrapping the redirect function.

User instuctions:

If user is not logged in:

![image](https://user-images.githubusercontent.com/65706419/201690395-858816ad-c43a-4348-838f-34404b1a5873.png)

User is requested to put in:
Long url - the url which shortened url will redirect to (only valid URL's are allowed
Expiration time -  date and time when this url will expire (only date in the future is allowed, a link won't be generated if the date is in the past)
Click limit - how many redirects are allowed (only positive intiger number's are allowed)

A short URL is generated for copy.

If the user is logged in or want's to use all the service functionallity:

![image](https://user-images.githubusercontent.com/65706419/201691790-267832e1-42c3-4913-b848-8ab90ab2e8b9.png)

User is requested to put his log in credentials or regisgter a new user

After a succesful login user is presented by the dashboard
![image](https://user-images.githubusercontent.com/65706419/201692160-78e797d6-7db6-4960-ab8a-87501a9891d8.png)

Same as in the anonymous user page a logged in user can create a new shortened URL, ant track it's statisticks.
Logged in user can: 
* press on short url link to get to the redirected page.
* Toggle url status, dissable or enable it.
* Delete url.
* Change expiration time of url.
* Track how much time is left till the link is expired.
* Check current number of ridirects of link.
* Get to info page

![image](https://user-images.githubusercontent.com/65706419/201692834-1a04f0eb-0bea-4449-906d-4652cf06241a.png)

In info page user's can:
* Which ip clicked on the redirect
* Who refered to this link
* What the link has been clicked
* Redirect time(in this current implementation redirect time is calculated by wrapping redirect function with the wrapper and callculating the execution time of the redirect function.






from django.core.mail import send_mail
from django.conf import settings

def send_approval_notifications(article):
    """
    Sends email notifications to subscribers and posts to Twitter.
    """
    # 1. Email Subscribers
    subscribers = set()
    
    # Publisher subscribers
    if article.publisher:
        pub_subs = article.publisher.subscribers.all()
        for user in pub_subs:
            if user.email:
                subscribers.add(user.email)
            
    # Journalist subscribers
    author_subs = article.author.journalist_subscribers.all()
    for user in author_subs:
        if user.email:
            subscribers.add(user.email)
        
    if subscribers:
        print(f"Sending emails to: {subscribers}") # Debug
        send_mail(
            subject=f"New Article: {article.title}",
            message=f"Read the new article by {article.author.username}.\n\n{article.content[:200]}...",
            from_email='news@example.com',
            recipient_list=list(subscribers),
            fail_silently=True
        )

    # 2. Post to Twitter
    post_to_twitter(article)

def post_to_twitter(article):
    """
    Posts the article to Twitter using a mock API or placeholder.
    """
    # Placeholder for Twitter API interaction
    print(f"Posting to Twitter: {article.title}")
    
    # Example structure for requests (commented out as we don't have tokens)
    # url = "https://api.twitter.com/2/tweets"
    # payload = {"text": f"New Article: {article.title} read more at..."}
    # headers = {
    #     "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    #     "Content-Type": "application/json"
    # }
    # response = requests.post(url, json=payload, headers=headers)
    # return response

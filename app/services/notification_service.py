class NotificationService:
    @staticmethod
    def notify(customer_email, message):
        print(f"Sending notification to {customer_email}: {message}")
from app.settings import STRIPE_API_KEY
from core.models import Item
import stripe 
stripe.api_key = STRIPE_API_KEY


# Inteface Class
class PaymentAPI:

    def create_session_id(self):
        '''Creates API Product'''
        raise NotImplementedError


# Stripe API Interface
class StripePaymentAPI(PaymentAPI):

    RETRY_COUNT = 3

    def create_product(self, django_instance: Item):
        try:
            stripe_product = stripe.Product.create(
                name=django_instance.name,
                description=django_instance.description
            )
            return stripe_product
        
        except Exception as e:
            print(f'Error creating Stripe Product: {e}')
            return {"error": e}
        

    def save_cached_product(self, stripe_product, django_instance:Item):
        if "error" in stripe_product:
            return 

        django_instance.stripe_id = stripe_product["id"]
        django_instance.save()


    def delete_product(self, django_instance: Item):
        if not django_instance.stripe_id:
            return 
        
        stripe.Product.delete(sid=django_instance.stripe_id)
        
        django_instance.stripe_id = ''
        django_instance.save()
    

    def create_price(self, django_instance: Item):
        if not django_instance.price or not django_instance.stripe_id:
            return {"error": f"No price field for {django_instance}"} 
        
        try:
            stripe_price = stripe.Price.create(
                unit_amount=int(django_instance.price.unit_price),
                currency=django_instance.price.currency.name if django_instance.price.currency else "eur",
                product=django_instance.stripe_id
            )
            return stripe_price
        except Exception as e:
            print(f'Error creating Stripe price: {e}')
            return {"error": e}            
        

    def delete_price(self, django_instance: Item):
        if not django_instance.price.stripe_id:
            return 
        
        django_instance.price.stripe_id = ''
        django_instance.price.save()


    def get_cached_price(self, price_id: str):
        try:
            return Item.objects.get(price__stripe_id=price_id)
        except:
            return None


    def save_cached_price(self, stripe_price, django_instance:Item):
        if not django_instance.price or "error" in stripe_price:
            return
        django_instance.price.stripe_id = stripe_price["id"] 
        django_instance.price.save()


    def create_session_id(self, django_instance: Item):

        if not django_instance.price:
            return None

        # check or create stripe product
        if not django_instance.stripe_id:
            stripe_product = self.create_product(django_instance)
            self.save_cached_product(stripe_product, django_instance)

        #check or create stripe price 
        if not django_instance.price.stripe_id:
            stripe_price = self.create_price(django_instance)
            self.save_cached_price(stripe_price, django_instance)
        
        
        session = None 
        retry_count = 0

        while True:

            if retry_count >= self.RETRY_COUNT or not django_instance.price.stripe_id:
                break

            try:
                session = stripe.checkout.Session.create(
                    success_url="https://example.com/success",
                    cancel_url="https://example.com/cancel",
                    line_items=[
                        {
                            "price": django_instance.price.stripe_id,
                            "quantity": 1,
                        },
                    ],
                    mode="payment",
                )
                break
            
            except Exception as e:
                print(f'error generation session: {e}')
                retry_count += 1
        
        return session
            
        

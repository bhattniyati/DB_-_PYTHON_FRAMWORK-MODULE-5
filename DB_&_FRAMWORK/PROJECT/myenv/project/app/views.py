from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
# Create your views here.

# Index Page
def index(request):
    return render(request,"index.html")
    
def addproduct(request):
    return render(request,"addproduct.html")

# Logic -- Addproduct
def insertproduct(request):
    if request.POST:
        id= Product_Mst.objects.create(product_name=request.POST['product_name'])
    if id:
        id= Product_Subcat.objects.create(

            product_id= id,
            product_price=request.POST["pprice"],
            product_image=request.FILES["pimage"],
            product_model=request.POST["pmodel"],
            product_ram=request.POST["pram"],
        )
        messages.success(request,"Product Added Successfully...")
        return redirect('show_product')
    else:
        return render(request,"addproduct.html")
    
# Logic -- Viewproduct
def showproduct(request):
    product= Product_Mst.objects.all()
    products= Product_Subcat.objects.all()
    return render(request,"showproduct.html",{'product':product,'products':products})

# Logic -- View Singleproduct

def singleproduct(request,pk):
    product= Product_Mst.objects.get(pk=pk)
    products= Product_Subcat.objects.filter(product_id=product)
    return render(request,"singleproduct.html",{'product':product,'products':products})

# Logic -- Deleteproduct
def deleteproduct(request,pk):
    product = Product_Mst.objects.get(pk=pk)
    product.delete()
    return redirect("show_product")

# Logic -- Updateproduct
def updateproduct(request, pk):
    product = Product_Mst.objects.get(pk=pk)
    products = Product_Subcat.objects.filter(product_id=product)

    if request.method == "POST":
        # Update Product_Mst field
        product.product_name = request.POST.get('product_name')

        # Update  Product_Subcat fields
        for prod in products:
            prod.product_price = request.POST.get('product_price')
            prod.product_model = request.POST.get('product_model')
            prod.product_ram = request.POST.get('product_ram')

            if 'product_image' in request.FILES:
                prod.product_image = request.FILES['product_image']

            # Save the updated Product_Subcat object
            prod.save()

        # Save the updated Product_Mst object
        product.save()
        return redirect('show_product')
    else:
        return render(request, 'updateproduct.html', {'product': product, 'products': products})

# Logic -- Searchproduct
def searchproduct(request):
    if request.POST:
        data= request.POST.get('product_name')
        print(data)
        if data:
            # Filter Product_Mst objects based on product name
            product= Product_Mst.objects.filter(product_name__contains=data)
            # Filter Product_Subcat objects based on product_id from filter Product_Mst objects
            products = Product_Subcat.objects.filter(product_id__in=product)
            return render(request,"searchproduct.html",{'product':product,'products':products})
        else:
            return render(request,"searchproduct.html")
        
    else:
            return render(request,"searchproduct.html")


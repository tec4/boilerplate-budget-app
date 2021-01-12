class Category:
  ledger = []
  categoryName = ""

  def __init__(self, categoryName):
    self.ledger = []
    self.categoryName = categoryName

  def deposit(self, amount, description = ''):
    self.ledger.append({
      "amount": amount, 
      "description": description
    })

  def withdraw(self, amount, description = ''):
    if self.check_funds(amount):
      self.ledger.append({
        "amount": -amount,
        "description": description
      })
      return True

    return False

  def get_balance(self):
    total = 0
    for item in self.ledger:
      total = total + item['amount']

    return total

  def transfer(self, amount, category):
    if self.withdraw(amount, 'Transfer to ' + category.categoryName):
      category.deposit(amount, 'Transfer from ' + self.categoryName)
      return True
    
    return False

  def check_funds(self, amount):
    return self.get_balance() >= amount

  def __str__(self):
    numStars = 30 - len(self.categoryName)
    perSide = int(numStars / 2)
    stars = ''.rjust(perSide, '*')

    objStr = stars + self.categoryName + stars + "\n"
    for item in self.ledger:
        # Take first 23 characters of description
        # If descrioption is not 23 characters in length, pad it w/ empty strings
        desc = item['description'][0:23].ljust(23, ' ')

        # Ensure amount is a float
        # Format float to two decimal places
        # RIght justify amount and pad string to 7 characrters
        amountStr = str("{:0.2f}".format(float(item['amount']))).rjust(7, ' ')

        objStr = objStr + desc + amountStr + "\n"

    return objStr + 'Total: ' + str(self.get_balance())


def create_spend_chart(categories):
  withdrawsByCategory = dict()
  totalWithdrawn = 0
  maxCategoryNameLen = 0
  for category in categories:
    if maxCategoryNameLen < len(category.categoryName):
        maxCategoryNameLen = len(category.categoryName)

    amountWithdrawn = 0
    for item in category.ledger:
        amount = item['amount']
        if amount < 0:
            # Subtracting negative from negative will yield a positive number
            # for the total amount withdrawn
            amountWithdrawn = amountWithdrawn - amount
          
    withdrawsByCategory[category.categoryName] = amountWithdrawn
    totalWithdrawn = totalWithdrawn + amountWithdrawn

  percetWithdrawn = dict()
  for category, amountWithdrawn in withdrawsByCategory.items():
    # Get percentage as whole number (ie: 0 through 100)
    # Divide by 10 and then multiple by 10 to round down to nearst 10th
    percetWithdrawn[category] = int(((amountWithdrawn / totalWithdrawn) * 100) / 10) * 10

  output = ''
  amounts = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
  for n in amounts:
      vals = []
      for category, percentage in percetWithdrawn.items():
        vals.append('o ' if percentage >= n else '  ')

      output = output + str(n).rjust(3, ' ') + '| ' + ' '.join(vals) + " \n"

  # Begin category name formatting
  output = output + '    ' + ('-' * (len(categories) * 3 + 1)) + "\n"
  for n in range(maxCategoryNameLen):
      output = output + '     '
      for category in categories:
          # Get character, if exists. Else empty space.
          if len(category.categoryName) - 1 >= n:
              output = output + category.categoryName[n]
          else:
             output = output + ' '

          # Add space between each category name
          output = output + '  '
      
      # Only print newline if not last iteration
      # Subtract 1 because range() starts at zero
      if n != (maxCategoryNameLen - 1):
          output = output + "\n"


  return "Percentage spent by category\n" + output

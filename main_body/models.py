from django.db import models


class Currency(models.Model):
    curr_list = models.CharField(max_length=150)
    bank_names_left = models.CharField(max_length=150)
    bank_names_right = models.CharField(max_length=150)
    prices_left = models.CharField(max_length=150)
    prices_right = models.CharField(max_length=150)

    def set_arguments(self, cur_list, bank_names_left, bank_names_right, prices_left, prices_right):
        self.curr_list = cur_list
        self.bank_names_right = bank_names_right
        self.bank_names_left = bank_names_left
        self.prices_right = prices_right
        self.prices_left = prices_left

    def __str__(self):
        return self.curr_list


class LastUpdatedDate(models.Model):
    date = models.DateTimeField()


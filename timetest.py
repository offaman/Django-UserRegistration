import time
import datetime




print((datetime.datetime.now() + datetime.timedelta(minutes=5)).time())



# # def delete_after_five_minutes(self):
# #             time = self.publishing_date + datetime.timedelta(minutes=1)
# #             if time < datetime.datetime.now():
# #                     e = Event.objects.get(pk=self.pk)
# #                     e.delete()
# #                     return True
# #             else:
# #                     return False


# def delete_after_five_minutes(self):
#                 time = self.publishing_date + datetime.timedelta(minutes=1)
#                 if time < datetime.datetime.now():
#                     e = Event.objects.get(pk=self.pk)
#                     e.delete()
#                     return True
#                 else:
#                     return False
#به نام ایزد منان
from .ORF import ORF, ORFDetector
#ORF Fwd را پیدا کن.(for RNA)
class ForwardORFDetector(ORFDetector):

    def detect(self):
        orfs = []   #لیست خالی برای اینکه اطلاعاتی که برنامه تولید میکند را در آن وارد کنیم
        #از لیست های استفاده کردیم چون که بعد ها در قسمت های دیگر برنامه تا بتوانیم هر مقدار
        # ORF که پیدا کردیم را درون اضافه کنیم در حالی که با index را به راحتی میتوانیم به آن دسترسی داشتهی باشم
        for frame in range(3): #رنج 3 برای بررسی 3 فریم

            i = frame

            while i <= len(self.sequence) - 3: #برای اینکه فقط برنامه فقط تا زمانی اجرا شود که کدون 3 حرفی موجود باشد

                codon = self.sequence[i:i + 3] #انتخاب کدون هایی با 3 کارکتر از رشته

                if codon == self.START_CODON:#تشخیص کدون آغاز

                    start_pos = i#آغاز عملیات
                    protein_sequence = []#ایجاد لیست برای ثبت رشته

                    j = i
                    #j مسئولیت پیمایش بر روی رشته بعد کدون آغار را دارد
                    while j <= len(self.sequence) - 3:

                        current_codon = self.sequence[j:j + 3] #برای اینکه فقط برنامه فقط تا زمانی اجرا شود که کدون 3 حرفی موجود باشد

                        if current_codon in self.STOP_CODONS:# تشخیص کدون پایان با تطبیق داد رشته با ست کدون های پایان
                            #اگر به کدون پایان رسیدیم اطلاعاتی که برنامه به آنهار رسیده را در درون پارامتر هایی که در تابع والد تعریف کردیم وارد میکنیم
                            orf = ORF(
                                strand="Forward",
                                frame=frame,
                                start_pos=start_pos,
                                protein=protein_sequence,
                                is_complete=True
                            )

                            orfs.append(orf) #افزودن ORF به orf
                            break


                        protein_sequence.append(current_codon)#اگر کدون استاپ نبود کدونی که یافت شده رو کنار بذار

                        j += 3 #عمل پیمایش 3 تایی را بعد از کدون آغاز انجام میدهد.


                    else:

                        orf = ORF(
                            strand="Forward",
                            frame=frame,
                            start_pos=start_pos,
                            protein=protein_sequence,
                            is_complete=False
                        )

                        orfs.append(orf)

                i += 3 #عمل پیمایش سه تایی قبل از کدون آغاز را انجام میدهد

        return orfs

                i += 3 #عمل پیمایش سه تایی قبل از کدون آغاز را انجام میدهد

        return orfs

from django.db import models

class User(models.Model):
    email = models.EmailField("Почта", max_length=255)
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    birth_date = models.DateField("Дата рождения")
    favorites = models.ManyToManyField('MediaContent', through='Favorite', verbose_name="Избранное")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class MediaContent(models.Model):
    CONTENT_TYPES = [
        ('MOVIE', 'Фильм'),
        ('SERIES', 'Сериал'),
    ]
    
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    release_date = models.DateField("Дата выхода")
    country = models.CharField("Страна производства", max_length=100)
    rating = models.FloatField("Рейтинг")
    age_restriction = models.PositiveIntegerField("Возрастное ограничение")
    duration = models.PositiveIntegerField("Длительность", null=True, blank=True) 
    content_type = models.CharField("Тип", max_length=10, choices=CONTENT_TYPES)
    genres = models.ManyToManyField('Genre', verbose_name="Жанры")

    class Meta:
        verbose_name = "Медиаконтент"
        verbose_name_plural = "Медиаконтент"

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    media_content = models.ForeignKey(MediaContent, verbose_name="Медиаконтент", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField("Оценка")
    review_text = models.TextField("Текст отзыва")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'media_content'],
                name='unique_user_media_review'
            )
        ]

    def __str__(self):  
        return f"Отзыв {self.user} на {self.media_content}"

class Favorite(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    media_content = models.ForeignKey(MediaContent, verbose_name="Медиаконтент", on_delete=models.CASCADE)
    added_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'media_content'],
                name='unique_user_media_favorite'
            )
        ]

    def __str__(self):  
        return f"{self.user} - {self.media_content}"

class ViewHistory(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    media_content = models.ForeignKey(MediaContent, verbose_name="Медиаконтент", on_delete=models.CASCADE, null=True, blank=True)
    episode = models.ForeignKey('Episode', verbose_name="Эпизод", on_delete=models.CASCADE, null=True, blank=True)  
    viewed_at = models.DateTimeField("Дата и время просмотра")
    viewed_seconds = models.PositiveIntegerField("Просмотрено секунд")

    class Meta:
        verbose_name = "История просмотров"
        verbose_name_plural = "История просмотров"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.media_content and not self.episode:
            raise ValidationError("Должен быть указан либо медиаконтент, либо эпизод")
        if self.media_content and self.episode:
            raise ValidationError("Можно указать только медиаконтент ИЛИ эпизод")

    def __str__(self):  
        content = self.media_content if self.media_content else self.episode
        return f"{self.user} - {content}"

class Subscription(models.Model):
    tariff_plan = models.CharField("Тарифный план", max_length=100)
    description = models.TextField("Описание")
    price = models.DecimalField("Стоимость", max_digits=8, decimal_places=2)
    duration = models.PositiveIntegerField("Длительность (дней)")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return self.tariff_plan

class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Активна'),
        ('EXPIRED', 'Истекла'),
        ('CANCELED', 'Отменена'),
    ]
    
    PAYMENT_METHODS = [ 
        ('CARD', 'Банковская карта'),
        ('PAYPAL', 'PayPal'),
        ('APPLE_PAY', 'Apple Pay'),
        ('GOOGLE_PAY', 'Google Pay'),
        ('YANDEX_MONEY', 'Яндекс.Деньги'),
    ]
    
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, verbose_name="Подписка", on_delete=models.CASCADE)
    status = models.CharField("Статус подписки", max_length=10, choices=STATUS_CHOICES)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    auto_renewal = models.BooleanField("Автопродление", default=False)
    payment_method = models.CharField("Способ оплаты", max_length=20, choices=PAYMENT_METHODS)  

    class Meta:
        verbose_name = "Подписка пользователя"
        verbose_name_plural = "Подписки пользователей"

    def __str__(self):  
        return f"{self.user} - {self.subscription} ({self.status})"

class Person(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    biography = models.TextField("Биография")
    media_content = models.ManyToManyField(MediaContent, through='ContentParticipation', verbose_name="Участие в контенте")

    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class ContentParticipation(models.Model):
    ROLE_CHOICES = [
        ('ACTOR', 'Актер'),
        ('DIRECTOR', 'Режиссер'),
        ('PRODUCER', 'Продюсер'),
        ('WRITER', 'Сценарист'),
        ('COMPOSER', 'Композитор'),
        ('OTHER', 'Другое'),
    ]
    
    media_content = models.ForeignKey(MediaContent, verbose_name="Медиаконтент", on_delete=models.CASCADE)
    person = models.ForeignKey(Person, verbose_name="Персона", on_delete=models.CASCADE)
    role = models.CharField("Роль", max_length=20, choices=ROLE_CHOICES)
    role_name = models.CharField("Название роли", max_length=100, null=True, blank=True)  

    class Meta:
        verbose_name = "Участие в контенте"
        verbose_name_plural = "Участие в контенте"

    def __str__(self):  
        return f"{self.person} - {self.media_content} ({self.role})"

class Genre(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    description = models.TextField("Описание жанра", blank=True)  

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name

class Season(models.Model):
    media_content = models.ForeignKey(MediaContent, verbose_name="Медиаконтент", on_delete=models.CASCADE)
    season_number = models.PositiveIntegerField("Номер сезона")
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"
        constraints = [
            models.UniqueConstraint(
                fields=['media_content', 'season_number'],
                name='unique_media_season'
            )
        ]

    def __str__(self):
        return f"{self.media_content.title} - Сезон {self.season_number}"

class Episode(models.Model):
    season = models.ForeignKey(Season, verbose_name="Сезон", on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField("Номер эпизода")
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    duration = models.PositiveIntegerField("Длительность")
    release_date = models.DateField("Дата выхода эпизода")

    class Meta:
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"
        constraints = [
            models.UniqueConstraint(
                fields=['season', 'episode_number'],
                name='unique_season_episode'
            )
        ]

    def __str__(self):
        return f"{self.season} - Эпизод {self.episode_number}: {self.title}"
# Django Test Toolkit

基于Django提供的一款测试工具箱。

## Features
- 支持模型测试数据生成
  - 支持根据对应数据模型快速生成测试数据
  - 支持自定义模型字段生成方式
  - 支持配置数据生成时默认值的采用比例
  - 支持配置唯一字段数据生成重复值时的重试次数
- 支持快速组合多种生命周期钩子
  - 内置account、blueking和drf等多种钩子
  - 支持快速自定义钩子并组合使用

## Quick Start

#### 数据生成示例

**定义模型数据生成工厂类**

最简单的情况，直接基于字段进行生成：

``` python
from django_test_toolkit.data_generation.faker_generator import DjangoModelFakerFactory

class ClockedTaskFactory(DjangoModelFakerFactory):
    class Meta:
        model = ClockedTask
```

如果需要对Model中的特定字段进行自定义，可以对Factory类进行修改：

``` python
import factory

class ClockedTaskFactory(DjangoModelFakerFactory):
    # 开发者自定义特定字段值
    notify_receivers = "fixed value"
    # 外键字段需要进行指定
    foreign_field = factory.SubFactory(ForeignModelFactory)
    
    class Meta:
        model = ClockedTask
```

**通过工厂类快速生成数据并插入测试数据库**

``` python
clocked_tasks = ClockedTaskFactory.create_batch(10)
```

此时会返回10个clocked_tasks对象，可供后续进行操作。

该步骤可以在测试准备阶段进行，如在setUpTestData等。

#### 接口测试示例（内置生命周期Mixin使用）

``` python
from django_test_toolkit.testcases import ToolkitApiTestCase
from django_test_toolkit.mixins.account import SuperUserMixin
from django_test_toolkit.mixins.blueking import LoginExemptMixin, StandardResponseAssertionMixin
from django_test_toolkit.mixins.drf import DrfPermissionExemptMixin

class ClockedTaskTestCase(
    ToolkitApiTestCase,
    SuperUserMixin,
    LoginExemptMixin,
    DrfPermissionExemptMixin,
    StandardResponseAssertionMixin,
):
    # DrfPermissionExemptMixin需要指定，用于豁免对应权限认证
    VIEWSET_PATH = "gcloud.clocked_task.viewset.ClockedTaskViewSet"
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # 生成数据并插入数据库
        cls.clocked_tasks = ClockedTaskFactory.create_batch(10)
        # 开发者自定义数据准备逻辑...
    
    def test_list_action_fetch_all_objects(self):
        url = reverse("clocked_task-list")
        response = self.client.get(url)
        # 由StandardResponseAssertionMixin提供，用于快速判断是否符合蓝鲸标准下请求成功的返回格式
        self.assertStandardSuccessResponse(response)
        # 判断list接口返回条数是否等于数据生成的条数
        self.assertEqual(len(response.data["data"]), len(self.clocked_tasks))

    def test_retrieve_action_fetch_specific_object(self):
        # 获取生成的第一条数据的id
        test_clocked_task = self.clocked_tasks[0]
        url = reverse("clocked_task-detail", args=[test_clocked_task.id])
        response = self.client.get(url)
        self.assertStandardSuccessResponse(response)
        # 判断retrieve接口请求的数据是否符合预期
        self.assertEqual(test_clocked_task.task_name, response.data["data"]["task_name"])
    
```

**注意：django_test_toolkit.testcases中的ToolkitApiTestCase或ToolkitTestCase需要放在继承顺序的第一位，将各个生命周期相关Mixin放在后面继承。**

#### 内置Mixin介绍

| Mixin名称                      | 相关领域    | 作用                                    | 涉及钩子                       | 配置项                                                       |
| ------------------------------ | ----------- | --------------------------------------- | ------------------------------ | ------------------------------------------------------------ |
| SuperUserMixin                 | 登陆        | 以admin身份登陆系统并进行后续client请求 | setUpTestData、setUp、tearDown | 无                                                           |
| DrfPermissionExemptMixin       | DRF ViewSet | 用于快速豁免ViewSet权限控制             | setUp                          | VIEWSET_PATH：测试类变量， 以字符串形式描述对应要豁免的ViewSet的路径 |
| LoginExemptMixin               | 蓝鲸        | 豁免蓝鲸登陆校验                        | setUp                          | 无                                                           |
| StandardResponseAssertionMixin | 蓝鲸        | 提供蓝鲸标准返回格式快速判断            | 无                             | 无                                                           |



## Extensions

#### 自定义生命周期Mixin

如果内置的Mixin无法满足需求，开发者可以基于LifeCycleHooksMixin进行开发，这样就可以让特定的逻辑与内置Mixin一样在对应的生命周期中被自动执行，可以大量复用于各个TestCase测试类中，也可实现多个Mixin的组合使用。

下面以内置生命周期Mixin：SuperUserMixin为例介绍如何进行自定义：

``` python
from django_test_toolkit.mixins.base import LifeCycleHooksMixin


class SuperUserMixin(LifeCycleHooksMixin):
    MOCK_SUPERUSER_NAME = "admin"
    MOCK_SUPERUSER_PASSWORD = "admin"

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        try:
            cls.superuser = user_model.objects.get(username=cls.MOCK_SUPERUSER_NAME)
        except user_model.DoesNotExist:
            cls.superuser = user_model.objects.create(
                username=cls.MOCK_SUPERUSER_NAME,
                password=cls.MOCK_SUPERUSER_PASSWORD,
                is_superuser=True,
                is_staff=True,
                is_active=True,
            )

    def setUp(self):
        self.client.force_login(user=self.superuser)

    def tearDown(self):
        self.client.logout()
```

1. 需要继承LifeCycleHooksMixin
2. 支持Django Test默认提供的生命周期钩子：setUpTestData、setUpClass、tearDownClass、setUp、tearDown
3. 在特定钩子中进行开发



#### 数据生成配置项

对于模型字段数据生成，django_test_toolkit中提供的默认配置：

``` python
DEFAULT_FIELD_TO_FAKER_CONFIG = {
    "fields": {
        "CharField": {"provider": "text", "processing_func": text_provider_char_field_processing},
        "TextField": {"provider": "text"},
        "IntegerField": {"provider": "random_int", "processing_func": random_int_provider_integer_field_processing},
        "DateTimeField": {
            "provider": "date_time_this_month",
            "extra_kwargs": {"tzinfo": pytz.utc, "before_now": True},
        },
    },
    "default_value_factor": DEFAULT_DEFAULT_VALUE_FACTOR,
    "unique_field_duplicate_retry_tolerance": DEFAULT_RETRY_TOLERANCE,
}
```

开发者可以在settings中设置变量**TEST_TOOLKIT_FAKER_CONFIG**来进行自定义配置，各配置项的含义如下表：

| 配置项                                    | 默认配置                                                     | 配置类型               | 含义                                                         |
| ----------------------------------------- | :----------------------------------------------------------- | ---------------------- | ------------------------------------------------------------ |
| fields                                    | 默认包含:<br />CharField<br />TextField<br />IntegerField<br />DateTimeField | dict                   | 各种模型字段的数据生成方式配置                               |
| fields.xxxField                           | 可包含:<br />provider(必填)<br />user_provider_class(选填)<br />processing_func(选填)<br />extra_kwargs(选填)<br />三个字段 | dict                   | 对应模型字段的数据生成方式具体配置                           |
| fields.xxxField.provider                  | 对应关系:<br />CharFiled: text<br />TextField: text<br />IntegerField:random_int<br />DateTimeField:date_time_this_month | str                    | 对应Faker的provider类型，可参考https://faker.readthedocs.io/en/master/providers/baseprovider.html，也可自定义 |
| fields.xxxField.user_provider_class(选填) | 无默认配置                                                   | faker.Provider类及子类 | 用户自定义provider类                                         |
| fields.xxxField.processing_func(选填)     | 对应配置:<br />CharField: 控制字段数据生成长度<br />IntegerField: 控制字段数据生成值区间 | 函数对象               | 对执行过程中才能确定的模型字段数据生成规则进行一些定制化开发，返回一个字典，将在Faker(provider).generate()中作为extra_kwargs参数 |
| fields.xxxField.extra_kwargs(选填)        | 对应配置:<br />DateTimeField: 默认时区为utc, 时间早于当前时间 | dict                   | 对执行前即可确认的数据生成规则进行配置，将在Faker(provider).generate()中作为extra_kwargs参数 |
| faker_data_locale(选填)                   | faker默认值，en_US                                           | str                    | faker数据生成默认使用的locale，需要对应的provider支持        |
| default_value_factor                      | 0.8                                                          | float                  | 当模型字段配置默认值时生成数据采用默认值的比例               |
| unique_field_duplicate_retry_tolerance    | 50                                                           | int                    | 当模型字段配置唯一属性时生成数据重复时的重试次数             |

#### 数据生成自定义Provider

基于faker.Provider，开发者可以定义适合业务特性的Provider来生成字段值。

为了方便演示，这里以faker官方文档中的DynamicProvider为例:

``` python
from faker.providers import DynamicProvider

medical_professions_provider = DynamicProvider(
    provider_name="medical_profession",
    elements=["dr.", "doctor", "nurse", "surgeon", "clerk"],
)
```

创建了自定义Provider之后，只需在配置项中指定对应的user_provider_class即可：

``` python
DEFAULT_FIELD_TO_FAKER_CONFIG = {
    "fields": {
        "CharField": {"provider": "medical_profession", "user_provider_class": medical_professions_provider},
        ...
    }
    ...
}
```

#### 数据生成自定义processing_func

因为Model各个字段会有一些自身的约束，为了能让自动生成的数据满足这些约束，有时候需要在faker数据生成过程中添加一些字段的约束逻辑，比如int的取值区间等，下面以random_int_provider_integer_field_processing为例说明应该如何实现自定义processing_func:

``` python
def random_int_provider_integer_field_processing(field):
    """传入model field对象作为参数, 返回约束参数字典，作为数据生成过程中的extra_kwargs"""
    extra_kwargs = {}
    # 从field的校验器中获取最大值和最小值，规定随机取值的区间
    for validator in field.validators:
        if validator.code in ["min_value", "max_value"]:
            extra_kwargs[validator.code.replace("_value", "")] = validator.limit_value
    return extra_kwargs
```


## Roadmap

- [版本日志](release.md)

## Support

- [蓝鲸论坛](https://bk.tencent.com/s-mart/community)
- [蓝鲸 DevOps 在线视频教程](https://cloud.tencent.com/developer/edu/major-100008)
- 联系我们，技术交流QQ群：

<img src="https://github.com/Tencent/bk-PaaS/raw/master/docs/resource/img/bk_qq_group.png" width="250" hegiht="250" align=center />


## BlueKing Community

- [BK-CI](https://github.com/Tencent/bk-ci)：蓝鲸持续集成平台是一个开源的持续集成和持续交付系统，可以轻松将你的研发流程呈现到你面前。
- [BK-BCS](https://github.com/Tencent/bk-bcs)：蓝鲸容器管理平台是以容器技术为基础，为微服务业务提供编排管理的基础服务平台。
- [BK-BCS-SaaS](https://github.com/Tencent/bk-bcs-saas)：蓝鲸容器管理平台SaaS基于原生Kubernetes和Mesos自研的两种模式，提供给用户高度可扩展、灵活易用的容器产品服务。
- [BK-PaaS](https://github.com/Tencent/bk-PaaS)：蓝鲸PaaS平台是一个开放式的开发平台，让开发者可以方便快捷地创建、开发、部署和管理SaaS应用。
- [BK-SOPS](https://github.com/Tencent/bk-sops)：标准运维（SOPS）是通过可视化的图形界面进行任务流程编排和执行的系统，是蓝鲸体系中一款轻量级的调度编排类SaaS产品。
- [BK-CMDB](https://github.com/Tencent/bk-cmdb)：蓝鲸配置平台是一个面向资产及应用的企业级配置管理平台。

## Contributing

如果你有好的意见或建议，欢迎给我们提 Issues 或 Pull Requests，为蓝鲸开源社区贡献力量。

[腾讯开源激励计划](https://opensource.tencent.com/contribution) 鼓励开发者的参与和贡献，期待你的加入。

## License

基于 MIT 协议， 详细请参考[LICENSE](LICENSE)

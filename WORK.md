Django 3.1.4 기준으로 test suite를 돌렸다.

configuration-aware 한 테스트는 configuration overwriting에 영향을 받지 않지만, 그냥 따로 filter-out 하진 않았다.

80a8be03d9 커밋이 3.1.4에 반영이 되어있지 않아
`schema.tests.SchemaTests.test_db_table` 테스트가 실패한다.

이를 cherrypick 한 후, 사용된 Mac 환경에 맞게끔 해당 커밋 의도를 살려
`supports_atomic_references_rename()` 리턴값을 False로 overriding 하였다.

Mac 환경에서 테스트를 돌리기 위해서는 아래 환경변수가 필요하다.

```sh
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

위의 설정을 마친 기본 test suite는 에러가 나지 않는다.

```sh
cat django/django/conf/global_settings.py | grep -E '= (True|False)$' | sed -E 's/ = (True|False)$/: True False/g' > input.txt
```

명령어를 이용하여 input params 리스트를 만들었다.

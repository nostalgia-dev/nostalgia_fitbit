
def test_import():
    import nostalgia_fitbit
    print(nostalgia_fitbit)
    assert nostalgia_fitbit.__version__ == '0.6.0'
    assert nostalgia_fitbit.FitbitClient

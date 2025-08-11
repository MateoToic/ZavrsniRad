def filtriranje(df, trajanje):
    ### uzme sve podatke kod kojih bar x minuta nije bilo promjene u brzini
    ### vraca df ['segment_id', 'start_time', 'end_time', 'duration', 'fan_speed_state']
    df['zone_fan_speed'] = df['zone_fan_speed'].replace(33.0, 33.3)
    df['zone_fan_speed'] = df['zone_fan_speed'].replace({
    0.0: 0,
    33.3: 1,
    66.5: 2,
    100.0: 3
    })
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')    
    piv = df.pivot_table(index='timestamp', 
                     columns='zone_id', 
                     values='zone_fan_speed', 
                     aggfunc='first')
    piv = piv.sort_index()
    piv = piv.bfill()
    changes_any_zone = piv.diff().ne(0).any(axis=1)     
    piv['segment_id'] = changes_any_zone.cumsum()
    df = df.set_index('timestamp')
    df = df.join(piv['segment_id'], how='inner')
    df = df.reset_index()
    segments = piv.groupby('segment_id', as_index=False).agg(
        start_time = ('segment_id', lambda x: x.index[0]),
        end_time   = ('segment_id', lambda x: x.index[-1])
    )
    segments['duration'] = segments['end_time'] - segments['start_time']
    fan_speed_po_segmentu = (
        df.groupby('segment_id')['zone_fan_speed']
        .agg(lambda x: x.dropna().iloc[0] if not x.dropna().empty else None)
        .reset_index()
        .rename(columns={'zone_fan_speed': 'fan_speed_state'})
    )
    segments = segments.merge(fan_speed_po_segmentu, on='segment_id', how='left')
    segments_novi = segments[segments['duration'] >= pd.Timedelta(minutes=trajanje)]
    return segments_novi
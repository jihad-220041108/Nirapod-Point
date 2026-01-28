import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

export const ProcessView1: React.FC = () => {
  const [active, setActive] = useState(false);
  const [data, setData] = useState<any[]>([]);
  
  useEffect(() => {
    setActive(true);
    return () => setActive(false);
  }, []);
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Subsystem {active ? 'Active' : 'Inactive'}</Text>
      <ScrollView>
        {data.map((d, i) => <Text key={i}>{JSON.stringify(d)}</Text>)}
      </ScrollView>
    </View>
  );
};

export const ProcessView2: React.FC = () => {
  const [active, setActive] = useState(false);
  const [data, setData] = useState<any[]>([]);
  
  useEffect(() => {
    setActive(true);
    return () => setActive(false);
  }, []);
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Subsystem {active ? 'Active' : 'Inactive'}</Text>
      <ScrollView>
        {data.map((d, i) => <Text key={i}>{JSON.stringify(d)}</Text>)}
      </ScrollView>
    </View>
  );
};

export const ProcessView3: React.FC = () => {
  const [active, setActive] = useState(false);
  const [data, setData] = useState<any[]>([]);
  
  useEffect(() => {
    setActive(true);
    return () => setActive(false);
  }, []);
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Subsystem {active ? 'Active' : 'Inactive'}</Text>
      <ScrollView>
        {data.map((d, i) => <Text key={i}>{JSON.stringify(d)}</Text>)}
